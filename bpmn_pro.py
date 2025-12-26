from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Iterable
import uuid
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Register namespaces to avoid prefix errors in parsers and tooling
ET.register_namespace('', 'http://www.omg.org/spec/BPMN/20100524/MODEL')
ET.register_namespace('bpmn', 'http://www.omg.org/spec/BPMN/20100524/MODEL')
ET.register_namespace('bpmndi', 'http://www.omg.org/spec/BPMN/20100524/DI')
ET.register_namespace('dc', 'http://www.omg.org/spec/DD/20100524/DC')
ET.register_namespace('di', 'http://www.omg.org/spec/DD/20100524/DI')

# Optional OpenAI import for schema extraction. The caller can pass content directly if preferred
try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


# -----------------------------
# Utilities
# -----------------------------

def _gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _slug(value: str, fallback: str = "item") -> str:
    s = re.sub(r"[^A-Za-z0-9_.-]+", "_", value or "").strip("_")
    return s[:64] or fallback


# -----------------------------
# Data structures (high-level schema)
# -----------------------------

@dataclass
class FlowElem:
    id: str
    type: str
    name: str = ""
    lane_id: Optional[str] = None
    outgoing: List[str] = field(default_factory=list)
    incoming: List[str] = field(default_factory=list)


@dataclass
class SequenceFlow:
    id: str
    sourceRef: str
    targetRef: str
    name: str = ""
    is_default: bool = False


@dataclass
class MessageFlow:
    id: str
    sourceRef: str
    targetRef: str
    name: str = ""


@dataclass
class Lane:
    id: str
    name: str


@dataclass
class Participant:
    id: str
    name: str
    processRef: str


@dataclass
class ProcessModel:
    id: str
    name: str
    lanes: List[Lane] = field(default_factory=list)
    elements: Dict[str, FlowElem] = field(default_factory=dict)
    flows: List[SequenceFlow] = field(default_factory=list)


@dataclass
class Collaboration:
    participants: List[Participant] = field(default_factory=list)
    message_flows: List[MessageFlow] = field(default_factory=list)


# -----------------------------
# BPMN Builder
# -----------------------------

class BPMNBuilder:
    def __init__(self, target_namespace: str = "http://bpmn.io/schema/bpmn") -> None:
        self.defs = ET.Element("definitions", attrib={
            "xmlns": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "xmlns:bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
            "xmlns:dc": "http://www.omg.org/spec/DD/20100524/DC",
            "xmlns:di": "http://www.omg.org/spec/DD/20100524/DI",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "id": _gen_id("Definitions"),
            "targetNamespace": target_namespace,
        })
        self.processes: Dict[str, ProcessModel] = {}
        self.collab = Collaboration()

    # ---- High-level authoring API ----
    def add_process(self, name: str) -> ProcessModel:
        pid = _gen_id("Process")
        model = ProcessModel(id=pid, name=name)
        self.processes[pid] = model
        return model

    def add_lane(self, process: ProcessModel, name: str) -> Lane:
        lane = Lane(id=_gen_id("Lane"), name=name)
        process.lanes.append(lane)
        return lane

    def add_participant(self, name: str, process: ProcessModel) -> Participant:
        part = Participant(id=_gen_id("Participant"), name=name, processRef=process.id)
        self.collab.participants.append(part)
        return part

    def add_element(self, process: ProcessModel, type_: str, name: str = "", lane: Optional[Lane] = None, elem_id: Optional[str] = None) -> FlowElem:
        eid = elem_id or _gen_id(type_)
        elem = FlowElem(id=eid, type=type_, name=name, lane_id=lane.id if lane else None)
        process.elements[eid] = elem
        return elem

    def connect(self, process: ProcessModel, source_id: str, target_id: str, name: str = "", is_default: bool = False) -> SequenceFlow:
        fid = _gen_id("Flow")
        flow = SequenceFlow(id=fid, sourceRef=source_id, targetRef=target_id, name=name, is_default=is_default)
        process.flows.append(flow)
        process.elements[source_id].outgoing.append(fid)
        process.elements[target_id].incoming.append(fid)
        return flow

    def add_message_flow(self, sourceRef: str, targetRef: str, name: str = "") -> MessageFlow:
        mf = MessageFlow(id=_gen_id("MessageFlow"), sourceRef=sourceRef, targetRef=targetRef, name=name)
        self.collab.message_flows.append(mf)
        return mf

    # ---- Validation ----
    def validate_process(self, process: ProcessModel) -> List[str]:
        errors: List[str] = []
        elems = process.elements
        # Rule: at least one startEvent
        if not any(e.type == "startEvent" for e in elems.values()):
            errors.append("Process must have at least one startEvent")
        # Rule: at least one endEvent
        if not any(e.type == "endEvent" for e in elems.values()):
            errors.append("Process must have at least one endEvent")
        # Unique IDs implicitly satisfied by dict keys
        # Flows must connect existing elements
        ids = set(elems.keys())
        for f in process.flows:
            if f.sourceRef not in ids:
                errors.append(f"Flow {f.id} sourceRef {f.sourceRef} does not exist")
            if f.targetRef not in ids:
                errors.append(f"Flow {f.id} targetRef {f.targetRef} does not exist")
        # No unconnected tasks (optional strictness)
        for e in elems.values():
            if e.type not in ("startEvent", "endEvent"):
                if not e.incoming and not e.outgoing:
                    errors.append(f"Element {e.id} ({e.name}) is not connected")
        return errors

    # ---- XML Generation ----
    def _emit_collaboration(self, parent: ET.Element) -> Optional[ET.Element]:
        if not self.collab.participants and not self.collab.message_flows:
            return None
        collab = ET.SubElement(parent, "collaboration", attrib={"id": _gen_id("Collab")})
        for p in self.collab.participants:
            ET.SubElement(collab, "participant", attrib={"id": p.id, "name": p.name, "processRef": p.processRef})
        for mf in self.collab.message_flows:
            attrs = {"id": mf.id, "sourceRef": mf.sourceRef, "targetRef": mf.targetRef}
            if mf.name:
                attrs["name"] = mf.name
            ET.SubElement(collab, "messageFlow", attrib=attrs)
        return collab

    def _emit_process(self, parent: ET.Element, process: ProcessModel) -> ET.Element:
        p = ET.SubElement(parent, "process", attrib={
            "id": process.id,
            "name": process.name,
            "isExecutable": "false",
        })
        if process.lanes:
            lane_set = ET.SubElement(p, "laneSet", attrib={"id": _gen_id("LaneSet")})
            for lane in process.lanes:
                l = ET.SubElement(lane_set, "lane", attrib={"id": lane.id, "name": lane.name})
                # BPMN lanes can contain flowNodeRef, but it's optional for minimal compatibility
        # Elements
        for e in process.elements.values():
            tag = e.type  # assume correct BPMN tag (startEvent, userTask, serviceTask, exclusiveGateway, etc.)
            attrs = {"id": e.id}
            if e.name:
                attrs["name"] = e.name
            el = ET.SubElement(p, tag, attrib=attrs)
            for inc in e.incoming:
                ET.SubElement(el, "incoming").text = inc
            for out in e.outgoing:
                ET.SubElement(el, "outgoing").text = out
        # Sequence flows
        for f in process.flows:
            attrs = {"id": f.id, "sourceRef": f.sourceRef, "targetRef": f.targetRef}
            if f.name:
                attrs["name"] = f.name
            sf = ET.SubElement(p, "sequenceFlow", attrib=attrs)
            if f.is_default:
                # Attach default on source element if gateway/task supports it
                src = process.elements.get(f.sourceRef)
                if src and src.type in ("exclusiveGateway", "inclusiveGateway", "complexGateway", "task", "userTask", "serviceTask", "scriptTask"):
                    # set default attribute on the source element
                    el = next((n for n in p.findall(".") if n.get("id") == src.id), None)
                    if el is not None:
                        el.set("default", f.id)
        return p

    def _auto_layout(self, processes: Iterable[ProcessModel]) -> ET.Element:
        # Very basic DI layout: elements arranged by lane (rows) and order-of-appearance (cols)
        bpmn_diagram = ET.SubElement(self.defs, "bpmndi:BPMNDiagram", attrib={"id": _gen_id("BPMNDiagram")})
        for process in processes:
            plane = ET.SubElement(bpmn_diagram, "bpmndi:BPMNPlane", attrib={
                "id": _gen_id("BPMNPlane"),
                "bpmnElement": process.id,
            })
            lane_index = {lane.id: idx for idx, lane in enumerate(process.lanes)}
            # group by lane
            grouped: Dict[Optional[str], List[FlowElem]] = {}
            for e in process.elements.values():
                grouped.setdefault(e.lane_id, []).append(e)
            # deterministic order by creation
            for lst in grouped.values():
                lst.sort(key=lambda x: x.id)
            # compute canvas width
            x_spacing, y_spacing = 180, 120
            x0, y0 = 120, 100
            max_cols = max((len(v) for v in grouped.values()), default=1)
            total_width = x0 + max_cols * x_spacing + 240
            # draw lane shapes
            for lane in process.lanes:
                row = lane_index[lane.id]
                lane_shape = ET.SubElement(plane, "bpmndi:BPMNShape", attrib={
                    "id": f"{lane.id}_di", "bpmnElement": lane.id,
                })
                ET.SubElement(lane_shape, "dc:Bounds", attrib={
                    "x": str(x0 - 80), "y": str(y0 + row * y_spacing - 20),
                    "width": str(total_width), "height": str(y_spacing)
                })
            # place elements and record centers
            centers: Dict[str, Tuple[int, int]] = {}
            for lane_id, elems in grouped.items():
                row = lane_index.get(lane_id, len(process.lanes))
                for col, e in enumerate(elems):
                    x = x0 + col * x_spacing
                    y = y0 + row * y_spacing
                    shape = ET.SubElement(plane, "bpmndi:BPMNShape", attrib={
                        "id": f"{e.id}_di", "bpmnElement": e.id,
                    })
                    w, h = (36, 36) if "Event" in e.type else (50, 50) if "Gateway" in e.type else (100, 60)
                    ET.SubElement(shape, "dc:Bounds", attrib={
                        "x": str(x), "y": str(y), "width": str(w), "height": str(h)
                    })
                    centers[e.id] = (x + w // 2, y + h // 2)
            # edges
            for f in process.flows:
                edge = ET.SubElement(plane, "bpmndi:BPMNEdge", attrib={"id": f"{f.id}_di", "bpmnElement": f.id})
                # straight line between recorded centers
                x1, y1 = centers.get(f.sourceRef, (0, 0))
                x2, y2 = centers.get(f.targetRef, (0, 0))
                ET.SubElement(edge, "di:waypoint", attrib={"x": str(x1), "y": str(y1)})
                ET.SubElement(edge, "di:waypoint", attrib={"x": str(x2), "y": str(y2)})
        return bpmn_diagram

    def to_xml(self) -> str:
        # Emit collaboration first (optional)
        self._emit_collaboration(self.defs)
        # Emit processes
        for p in self.processes.values():
            self._emit_process(self.defs, p)
        # Auto layout
        self._auto_layout(self.processes.values())
        # Pretty print
        xml_string = ET.tostring(self.defs, encoding="unicode")
        dom = minidom.parseString(xml_string)
        pretty = dom.toprettyxml(indent="  ")
        pretty = "\n".join([line for line in pretty.split("\n") if line.strip()])
        return pretty


# -----------------------------
# OpenAI-assisted extraction (optional)
# -----------------------------

DEFAULT_SCHEMA_PROMPT = (
    """
    You are a BPMN 2.0 expert. Extract a professional process model with pools, lanes, tasks, gateways, events,
    sequence flows and message flows from the description provided.

    Return STRICT JSON with this schema (no markdown):
    {
      "collaboration": {
        "participants": [ {"name": "<pool name>", "process_name": "<process name>"} ]
      },
      "processes": [
        {
          "name": "<process name>",
          "lanes": [ {"name": "<lane name>"} ],
          "elements": [
            {"id": "<string>", "type": "startEvent|endEvent|task|userTask|serviceTask|scriptTask|exclusiveGateway|parallelGateway|inclusiveGateway|intermediateCatchEvent|intermediateThrowEvent", "name": "<label>", "lane": "<lane name>"}
          ],
          "flows": [
            {"source": "<element id>", "target": "<element id>", "name": "<condition or label>", "default": false}
          ]
        }
      ],
      "message_flows": [
        {"source": "<participant name or element id>", "target": "<participant name or element id>", "name": "<label>"}
      ]
    }

    Rules:
    - Exactly one startEvent per process; at least one endEvent per process.
    - Use gateways for decisions and parallelization. Set one outgoing flow as default where applicable.
    - Assign every element to a lane if lanes are provided.
    - Prefer specific task types (userTask, serviceTask) when clear.
    """
)


def generate_bpmn_from_description(description: str, openai_api_key: str, schema_prompt: str = DEFAULT_SCHEMA_PROMPT) -> str:
    if OpenAI is None:
        raise RuntimeError("openai package not available. Install openai>=1.0")

    client = OpenAI(api_key=openai_api_key)
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Professional BPMN modeler"},
                  {"role": "user", "content": f"{schema_prompt}\n\nPROCESS DESCRIPTION:\n{description}"}],
        response_format={"type": "json_object"},
        temperature=0.1,
        max_tokens=2000,
    )
    import json
    spec = json.loads(resp.choices[0].message.content or "{}")

    builder = BPMNBuilder()

    # Build participants/processes
    participant_map: Dict[str, Participant] = {}
    process_by_name: Dict[str, ProcessModel] = {}

    for p_spec in spec.get("processes", []):
        p = builder.add_process(p_spec.get("name") or "Process")
        process_by_name[p_spec.get("name", p.id)] = p
        # lanes
        lane_map: Dict[str, Lane] = {}
        for l in p_spec.get("lanes", []):
            lane = builder.add_lane(p, l.get("name") or "Lane")
            lane_map[lane.name] = lane
        # elements
        elem_ids: Dict[str, FlowElem] = {}
        for e in p_spec.get("elements", []):
            lane_ref = lane_map.get(e.get("lane") or "") if lane_map else None
            elem = builder.add_element(
                p,
                type_=e.get("type", "task"),
                name=e.get("name") or "",
                lane=lane_ref,
                elem_id=e.get("id") if e.get("id") else None,
            )
            elem_ids[elem.id] = elem
        # flows
        for f in p_spec.get("flows", []):
            src = f.get("source")
            tgt = f.get("target")
            if src in elem_ids and tgt in elem_ids:
                builder.connect(p, src, tgt, name=f.get("name") or "", is_default=bool(f.get("default")))
        # participant for this process (optional via collaboration spec)
    for part in (spec.get("collaboration", {}) or {}).get("participants", []):
        pname = part.get("name") or "Participant"
        proc_name = part.get("process_name")
        proc = process_by_name.get(proc_name) or next(iter(builder.processes.values()))
        participant_map[pname] = builder.add_participant(pname, proc)

    # message flows
    for mf in spec.get("message_flows", []) or []:
        src = mf.get("source")
        tgt = mf.get("target")
        if not (src and tgt):
            continue
        # allow participant names or element IDs
        src_id = participant_map.get(src).id if src in participant_map else src
        tgt_id = participant_map.get(tgt).id if tgt in participant_map else tgt
        builder.add_message_flow(src_id, tgt_id, name=mf.get("name") or "")

    # Validate
    errors: List[str] = []
    for p in builder.processes.values():
        errors.extend(builder.validate_process(p))
    if errors:
        # Not fatal; include as XML comment head
        comment = ET.Comment("Validation warnings: " + " | ".join(errors))
        builder.defs.insert(0, comment)

    return builder.to_xml()
