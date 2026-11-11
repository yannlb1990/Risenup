(() => {
  const form = document.querySelector("#capacity-form");
  if (!form) return;

  const $ = (selector) => document.querySelector(selector);
  const inputs = {
    sales: $("#annual-sales"),
    labour: $("#annual-labour"),
    bookable: $("#bookable-hours"),
    delivered: $("#delivered-hours"),
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

    const core = [sales, bookable, delivered];
    if ([...core, labour, variable].some((n) => n !== null && (!Number.isFinite(n) || n < 0))) {
      message.textContent = "Enter zero or a positive number in each field.";
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }
    if ((sales ?? 0) > 100_000_000 || (labour ?? 0) > 100_000_000 || (bookable ?? 0) > 10_000 || (delivered ?? 0) > 10_000) {
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
    if (!sales || !bookable || !delivered) {
      emptyResult.hidden = false;
      result.hidden = true;
      return;
    }

    const utilisation = Math.min(100, (delivered / bookable) * 100);
    const salesPerHour = sales / (delivered * 52);
    const availableLift = Math.max(0, 100 - utilisation);
    const appliedLift = Math.min(lift, availableLift);
    const extraHours = bookable * (appliedLift / 100);
    const scenarioSales = extraHours * salesPerHour * 52;

    $("#scenario-sales").textContent = money(scenarioSales);
    $("#scenario-description").textContent = `Based on ${extraHours.toFixed(1)} additional delivered hours per week, at your current average service sales per delivered hour.`;
    $("#current-utilisation").textContent = pct(utilisation);
    $("#labour-share").textContent = labour === null ? "Add figure" : pct(sales > 0 ? (labour / sales) * 100 : 0);
    $("#sales-per-hour").textContent = money(salesPerHour);
    $("#extra-hours").textContent = extraHours.toFixed(1);
    emptyResult.hidden = true;
    result.hidden = false;

    const contributionCard = $("#contribution-card");
    contributionCard.hidden = variable === null;
    if (variable !== null) {
      $("#scenario-contribution").textContent = money(scenarioSales * (1 - variable / 100));
    }
    const capNote = $("#capacity-cap-note");
    capNote.hidden = appliedLift >= lift;
    if (!capNote.hidden) capNote.textContent = `The selected improvement exceeds your remaining capacity, so this scenario is capped at ${pct(availableLift)}.`;
  }

  form.addEventListener("input", update);
  form.addEventListener("submit", (event) => event.preventDefault());
  $("#print-scenario")?.addEventListener("click", () => window.print());
  update();
})();
