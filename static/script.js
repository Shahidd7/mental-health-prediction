  const form = document.getElementById("form");
  const button = document.getElementById("submit");
  const scoreEl = document.getElementById("score");
  const bar = document.getElementById("bar");
  const interpretation = document.getElementById("interpretation");
  const errorEl = document.getElementById("error");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorEl.textContent = "";
    button.disabled = true;
    button.textContent = "Predicting...";

    const fd = new FormData(form);
    const payload = {
      Age: Number(fd.get("Age")),
      Gender: fd.get("Gender"),
      Academic_Level: fd.get("Academic_Level"),
      most_used_platform: fd.get("most_used_platform"),
      purpose_of_use: fd.get("purpose_of_use"),
      Avg_Daily_Usage_Hours: Number(fd.get("Avg_Daily_Usage_Hours")),
      Daily_Unlocks: Number(fd.get("Daily_Unlocks")),
      Study_Hours: Number(fd.get("Study_Hours")),
      Physical_Activity_Hours: Number(fd.get("Physical_Activity_Hours")),
      Sleep_Hours_Per_Night: Number(fd.get("Sleep_Hours_Per_Night")),
      Stress_Level: fd.get("Stress_Level")
      };

      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail ? JSON.stringify(data.detail) : "Prediction failed.");

        const score = Number(data.predicted);
        scoreEl.textContent = score.toFixed(2);
        bar.style.width = Math.max(0, Math.min(100, score)) + "%";

        const percentage = Math.max(0, Math.min(10, score)) * 10;
bar.style.width = percentage + "%";

if (score < 4) {
    interpretation.textContent =
        "Lower predicted score — consider reviewing the lifestyle factors entered.";
} 
else if (score < 7) {
    interpretation.textContent =
        "Moderate predicted score — keep an eye on stress, sleep and daily habits.";
} 
else {
    interpretation.textContent =
        "Higher predicted score — the model estimates a relatively stronger mental-health score.";
}

      } catch (err) {
        errorEl.textContent = "Could not get a prediction. Make sure FastAPI is running and the model loaded successfully.";
        console.error(err);
      } finally {
        button.disabled = false;
        button.textContent = "Predict mental health score";
      }
    });
