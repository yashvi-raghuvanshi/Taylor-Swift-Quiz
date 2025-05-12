 async function submitQuiz() {
  const answers = {
    genre: document.getElementById("q1").value,
    music_feeling: document.getElementById("q2").value,
    taylor_era: document.getElementById("q3").value,
    concert_experience: document.getElementById("q4").value,
    lyrical_vibe: document.getElementById("q5").value,
    daily_soundtrack: document.getElementById("q6").value
  };

  try {
    const response = await fetch("http://localhost:8000/recommend_song", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(answers)
    });

    const data = await response.json();
    document.getElementById("result").textContent =
      `Your Taylor Swift song is: "${data.recommended_song}"`;
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("result").textContent =
      "Couldn't fetch your song. Please try again.";
  }
}