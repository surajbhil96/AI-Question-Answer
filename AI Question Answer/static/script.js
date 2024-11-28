document.getElementById("question-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const topic = document.getElementById("topic").value;
    const response = await fetch("/generate_question", {
        method: "POST",
        body: new URLSearchParams({ topic }),
    });
    const data = await response.json();
    if (data.question) {
        document.getElementById("generated-question").innerText = data.question;
        document.getElementById("question-area").style.display = "block";
    } else {
        alert(data.error || "Failed to generate question!");
    }
});
document.getElementById("answer-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const question = document.getElementById("generated-question").innerText;
    const answer = document.getElementById("answer").value;
    const response = await fetch("/validate_answer", {
        method: "POST",
        body: new URLSearchParams({ question, answer }),
    });
    const data = await response.json();
    document.getElementById("validation-result").innerText =
        data.validation || data.error || "Validation failed!";
});