(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function round1(x) { return Math.round(x * 10) / 10; }

  function roomPlan(lengthM, widthM, heightM, factor) {
    if (!(lengthM > 0) || !(widthM > 0) || !(heightM > 0) || !(factor > 0)) return { error: "length, width, height and factor must be positive" };
    var volume = lengthM * widthM * heightM;
    var watts = Math.round(volume * factor);
    var btu = Math.round(watts * 3.412);
    var verdict;
    if (watts < 600) verdict = "a small panel covers it";
    else if (watts < 1500) verdict = "one standard panel covers it";
    else if (watts < 3000) verdict = "one large or two smaller panels share it";
    else verdict = "several radiators share the load";
    return { volume: round1(volume), watts: watts, btu: btu, verdict: verdict };
  }

  function deltaPlan(flowC, returnC, roomC, ratedW) {
    if (!(flowC > 0) || !(returnC > 0) || !(roomC > 0) || !(ratedW > 0)) return { error: "flow, return, room and rating must be positive" };
    var mean = round1((flowC + returnC) / 2);
    var dt = round1(mean - roomC);
    if (dt <= 0) return { error: "the water must be warmer than the room" };
    var factor, verdict;
    if (dt >= 50) { factor = 1.0; verdict = "full rated output on the labeled table"; }
    else if (dt >= 40) { factor = 0.75; verdict = "three quarters on the labeled table"; }
    else if (dt >= 30) { factor = 0.51; verdict = "about half on the labeled table"; }
    else if (dt >= 20) { factor = 0.3; verdict = "under a third on the labeled table"; }
    else { factor = 0.12; verdict = "a trickle on the labeled table"; }
    var real = Math.round(ratedW * factor);
    return { mean: mean, dt: dt, factor: factor, real: real, verdict: verdict };
  }

  function sectionPlan(neededW, perSectionW) {
    if (!(neededW > 0) || !(perSectionW > 0)) return { error: "need and section output must be positive" };
    var sections = Math.ceil(neededW / perSectionW);
    var total = sections * perSectionW;
    var spare = total - neededW;
    var verdict;
    if (sections <= 8) verdict = "a compact radiator covers it";
    else if (sections <= 16) verdict = "a standard column covers it";
    else verdict = "a long column - two smaller radiators share the load";
    return { sections: sections, total: total, spare: spare, verdict: verdict };
  }

  function renderRoom(r, lengthM, widthM, heightM, factor) {
    return "A room " + lengthM + " m x " + widthM + " m x " + heightM + " m holds " + r.volume + " m3; at a labeled " + factor + " W per m3 it asks for about " + plural(r.watts, "watt") + " (" + plural(r.btu, "BTU", "BTU") + ") - " + r.verdict + ".";
  }

  function renderDelta(r, flowC, returnC, roomC, ratedW) {
    return "Flow " + flowC + " C, return " + returnC + " C and a " + roomC + " C room put the mean water at " + r.mean + " C, " + r.dt + " C above the room: a radiator rated at " + plural(ratedW, "watt") + " gives about " + plural(r.real, "watt") + " here - " + r.verdict + ".";
  }

  function renderSection(r, neededW, perSectionW) {
    return plural(neededW, "watt") + " needed, " + plural(perSectionW, "watt") + " a section: " + plural(r.sections, "section") + ", " + plural(r.total, "watt") + " total, " + plural(r.spare, "watt") + " of headroom - " + r.verdict + ".";
  }

  var api = { roomPlan: roomPlan, deltaPlan: deltaPlan, sectionPlan: sectionPlan, renderRoom: renderRoom, renderDelta: renderDelta, renderSection: renderSection };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.RadiatorMath = api;
})(this);
