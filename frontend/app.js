// GlassBox frontend logic: collect the form, call /api/estimate,
// and render the response into the results panel.

const glass = document.getElementById("glass");
const form = document.getElementById("estimate-form");
const submitButton = document.getElementById("submit-button");
const formError = document.getElementById("form-error");
const resultsEl = document.getElementById("results");

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function formatCurrency(amount) {
  return currencyFormatter.format(amount);
}

function buildFeedRow(entry) {
  const row = document.createElement("div");
  row.className = "feed-row";
  row.innerHTML = `
    <span class="feed-meta">
      <strong>${entry.name}</strong> · ${entry.plan_label} · ${entry.channel} · ${entry.time_ago}
    </span>
    <span class="feed-amount">+${formatCurrency(entry.amount)}</span>
  `;
  return row;
}

function buildBubble(message) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${message.sender}`;
  bubble.textContent = message.text;
  return bubble;
}

function renderResults(data) {
  resultsEl.innerHTML = "";

  // Recovery potential. At very low lead volumes the conservative and
  // expected figures can round to the same displayed value — show a
  // single number rather than a confusing "$X - $X" range.
  const conservativeDisplay = formatCurrency(data.conservative_monthly_revenue);
  const expectedDisplay = formatCurrency(data.expected_monthly_revenue);
  const revenueDisplay =
    conservativeDisplay === expectedDisplay
      ? conservativeDisplay
      : `${conservativeDisplay}<span class="divider">&ndash;</span>${expectedDisplay}`;

  const revenueCard = document.createElement("section");
  revenueCard.className = "result-card";
  revenueCard.innerHTML = `
    <h2>Recovery potential</h2>
    <div class="revenue-range">${revenueDisplay}</div>
    <p class="revenue-caption">Estimated recovered revenue per month</p>
  `;
  resultsEl.appendChild(revenueCard);

  // Live recovery feed preview
  const feedCard = document.createElement("section");
  feedCard.className = "result-card";
  const feedHeading = document.createElement("h2");
  feedHeading.textContent = "Your live recovery feed (preview)";
  feedCard.appendChild(feedHeading);

  const feedList = document.createElement("div");
  feedList.className = "feed-list";
  data.sample_feed.forEach((entry) => feedList.appendChild(buildFeedRow(entry)));
  feedCard.appendChild(feedList);
  resultsEl.appendChild(feedCard);

  // Sample conversation
  const conversationCard = document.createElement("section");
  conversationCard.className = "result-card";
  const conversationHeading = document.createElement("h2");
  conversationHeading.textContent = "Sample conversation";
  conversationCard.appendChild(conversationHeading);

  const conversation = document.createElement("div");
  conversation.className = "conversation";
  data.sample_conversation.forEach((message) => conversation.appendChild(buildBubble(message)));
  conversationCard.appendChild(conversation);
  resultsEl.appendChild(conversationCard);

  // Call to action
  const ctaCard = document.createElement("section");
  ctaCard.className = "result-card cta";
  ctaCard.innerHTML = `
    <a class="cta-button" href="#book-a-call">Book a call to model this for real</a>
    <p class="cta-caption">${data.disclaimer}</p>
  `;
  resultsEl.appendChild(ctaCard);

  // Reveal as one orchestrated moment: the box drops its "frosted" look
  // right as the results fade + settle into place, rather than each
  // card animating in on its own.
  resultsEl.hidden = false;
  glass.dataset.state = "clear";
  requestAnimationFrame(() => resultsEl.classList.add("is-visible"));
}

async function handleSubmit(event) {
  event.preventDefault();
  formError.hidden = true;

  const formData = new FormData(form);
  const payload = {
    monthly_abandoned_leads: Number(formData.get("monthly_abandoned_leads")),
    average_order_value: Number(formData.get("average_order_value")),
    funnel_stage: formData.get("funnel_stage"),
    follow_up_method: formData.get("follow_up_method"),
  };

  submitButton.disabled = true;
  submitButton.textContent = "Calculating…";
  glass.classList.add("is-calculating");

  try {
    const response = await fetch("/api/estimate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    renderResults(data);
    form.hidden = true;
  } catch (error) {
    formError.textContent = "Something went wrong generating your estimate. Please try again.";
    formError.hidden = false;
    glass.dataset.state = "frosted";
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "See my recovery potential";
    glass.classList.remove("is-calculating");
  }
}

form.addEventListener("submit", handleSubmit);
