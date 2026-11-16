(() => {
  const form = document.querySelector("#capacity-form");
  if (!form) return;

  const $ = (selector) => document.querySelector(selector);
  const inputs = {
    sales: $("#annual-sales"),
    labour: $("#annual-labour"),
    bookable: $("#bookable-hours"),
    delivered: $("#delivered-hours"),
    weeks: $("#weeks-open"),
    variable: $("#variable-cost"),
    lift: $("#utilisation-lift"),
  };
  const emptyResult = $("#empty-result");
  const result = $("#scenario-result");
  const message = $("#form-message");
  const money = (value) => new Intl.NumberFormat("en-AU", {
    style: "currency", currency: "AUD", maximumFractionDigits: 0,
  }).format(Number.isFinite(value) ? value : 0);
  const pct = (value) => `${value.toFixed(1)}%`;
  const value = (input) => input.value.trim() === "" ? null : Number(input.value);

  function update() {
    const sales = value(inputs.sales);
    const labour = value(inputs.labour);
    const bookable = value(inputs.bookable);
    const delivered = value(inputs.delivered);
    const variable = value(inputs.variable);
    const lift = Number(inputs.lift.value);
    $("#lift-output").textContent = `+${lift} ${lift === 1 ? "point" : "points"}`;
    message.textContent = "";

    const weeks = value(inputs.weeks);
    const core = [sales, bookable, delivered, weeks];
    if ([...core, labour, variable].some((n) => n !== null && (!Number.isFinite(n) || n < 0))) {
      message.textContent = "Enter zero or a positive number in each field.";
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }
    if ((sales ?? 0) > 100_000_000 || (labour ?? 0) > 100_000_000 || (bookable ?? 0) > 10_000 || (delivered ?? 0) > 10_000 || (weeks ?? 0) > 52) {
      message.textContent = "Please check the figures. One value is above the range this tool can calculate.";
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }
    if (variable !== null && variable > 100) {
      message.textContent = "Direct variable costs must be 100% or less. Clear the field if you do not know the figure.";
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }
    if (bookable !== null && delivered !== null && delivered > bookable) {
      message.textContent = "Delivered hours can’t be higher than bookable hours. Check that both figures cover the same team and week.";
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }
    if (!sales || !bookable || !delivered || !weeks) {
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }

    const utilisation = Math.min(100, (delivered / bookable) * 100);
    const salesPerHour = sales / (delivered * weeks);
    const availableLift = Math.max(0, 100 - utilisation);
    const appliedLift = Math.min(lift, availableLift);
    const extraHours = Math.min(bookable * (appliedLift / 100), Math.max(0, bookable - delivered));
    const scenarioSales = extraHours * salesPerHour * weeks;
    const capacityCeiling = Math.max(0, bookable - delivered) * salesPerHour * weeks;

    $("#scenario-sales").textContent = money(scenarioSales);
    $("#scenario-description").textContent = `If you filled ${extraHours.toFixed(1)} more service hours a week across ${weeks} working weeks, at your current average sales per delivered hour.`;
    $("#current-utilisation").textContent = pct(utilisation);
    $("#labour-share").textContent = labour === null ? "Add figure" : pct(sales > 0 ? (labour / sales) * 100 : 0);
    $("#sales-per-hour").textContent = money(salesPerHour);
    $("#extra-hours").textContent = extraHours.toFixed(1);
    $("#capacity-ceiling").textContent = money(capacityCeiling);
    const bookedWidth = Math.max(0, Math.min(100, utilisation));
    const scenarioWidth = Math.max(0, Math.min(100 - bookedWidth, (extraHours / bookable) * 100));
    $("#capacity-meter-used").style.width = `${bookedWidth}%`;
    $("#capacity-meter-scenario").style.width = `${scenarioWidth}%`;
    $("#capacity-meter-label").textContent = `${delivered.toFixed(1)} of ${bookable.toFixed(1)} hours currently delivered`;
    $("#capacity-meter").setAttribute("aria-label", `${delivered.toFixed(1)} of ${bookable.toFixed(1)} bookable hours delivered; ${extraHours.toFixed(1)} extra hours included in this scenario`);
    emptyResult.hidden = true;
    result.hidden = false;

    const contributionCard = $("#contribution-card");
    contributionCard.hidden = variable === null;
    if (variable !== null) {
      $("#scenario-contribution").textContent = money(scenarioSales * (1 - variable / 100));
    }
    const capNote = $("#capacity-cap-note");
    capNote.hidden = appliedLift >= lift;
    if (!capNote.hidden) capNote.textContent = `The selected improvement is higher than your currently unfilled time, so the scenario is capped at ${pct(availableLift)} utilisation.`;
  }

  form.addEventListener("input", update);
  form.addEventListener("submit", (event) => event.preventDefault());
  $("#print-scenario")?.addEventListener("click", () => window.print());
  update();

  const questions = [...document.querySelectorAll(".check-question")];
  const progress = $("#check-progress");
  const progressLabel = $("#check-progress-label");
  const checkResult = $("#check-result");
  const answer = (name) => document.querySelector(`input[name="${name}"]:checked`)?.value;
  const areas = {
    demand: "booking demand and the appointment times clients are looking for",
    numbers: "service prices and the time and direct costs behind each booking",
    time: "a repeated admin task and whether a simpler way of handling it would help",
    systems: "how your current tools share information and where work is being repeated",
  };
  const supportingClues = [];
  function updateBusinessCheck() {
    const answered = questions.filter((fieldset) => fieldset.querySelector("input:checked")).length;
    progress.value = answered;
    progressLabel.textContent = `${answered} of ${questions.length} answered`;
    checkResult.hidden = answered < questions.length;
    if (checkResult.hidden) return;

    const focus = areas[answer("priority")];
    supportingClues.length = 0;
    const gaps = answer("gaps");
    const numbers = answer("service-numbers");
    const time = answer("time");
    const systems = answer("systems");
    if (["often", "sometimes"].includes(gaps)) supportingClues.push("when appointment gaps show up");
    if (["hunch", "unclear"].includes(numbers)) supportingClues.push("which services cover the time and direct costs they use");
    if (["double-entry", "coordination", "owner"].includes(time)) supportingClues.push("where a hand-off or repeated task slows the day down");
    if (["some-manual", "disconnected", "unsure"].includes(systems)) supportingClues.push("what information your current apps can share");
    if (!supportingClues.length) supportingClues.push("how to protect what is already working as the business grows");

    $("#check-result-title").textContent = "A useful first conversation";
    $("#check-result-copy").textContent = `You said ${focus} matters most. It may help to explore that alongside ${supportingClues.slice(0, 2).join(" and ")}. We can shape the work around your business after understanding the details.`;
  }
  document.querySelectorAll(".check-question input").forEach((input) => input.addEventListener("change", updateBusinessCheck));
  updateBusinessCheck();
})();
