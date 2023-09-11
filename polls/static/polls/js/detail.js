const toggleChoice = (button, choiceId) => {
  const choiceInput = document.querySelector(`input[name="choice"][value="${choiceId}"]`);

  const selectedChoice2 = document.getElementById("selected-choice-1");

  if (selectedChoice2 !== null) {
    if (choiceInput) {
      // already selected -> unselect it
      if (choiceInput.checked) {
        choiceInput.checked = false;
        button.classList.remove("bg-green-500", "border-solid", "border-2", "border-black", "hover:bg-green-600");
        button.classList.add("bg-white", "border-solid", "border-2", "border-black", "hover:bg-white");
        // Clear display
        document.getElementById("selected-choice-1").textContent = "You have been voted😊 Anyway, you can change the choice anytime before end date";
      } else {
        // Unselect all choices
        document.querySelectorAll('input[name="choice"]').forEach(choice => {
          choice.checked = false;
        });

        // Select the clicked choice
        choiceInput.checked = true;

        // Reset the style of all choice buttons
        document.querySelectorAll(".choice-button").forEach(btn => {
          btn.classList.remove("bg-green-500", "border-solid", "border-2", "border-black", "hover:bg-green-600");
          btn.classList.add("bg-white", "border-solid", "border-2", "border-black", "hover:bg-white");
        });

        button.classList.remove("bg-white", "border-solid", "border-2", "border-black", "hover:bg-white");
        button.classList.add("bg-green-500", "border-solid", "border-2", "border-black", "hover:bg-green-600");

        const choiceText = button.textContent.trim();
        document.getElementById("selected-choice-1").textContent = `You select: ${choiceText}`;
      }
    }
    // Enable the "Vote" button -> if select
    const voteButton = document.getElementById("vote-button");
    voteButton.disabled = !document.querySelector('input[name="choice"]:checked');
  } else {
    if (choiceInput) {
      // already selected -> unselect it
      if (choiceInput.checked) {
        choiceInput.checked = false;
        button.classList.remove("bg-green-500", "border-solid", "border-2", "border-black", "hover:bg-green-600");
        button.classList.add("bg-white", "border-solid", "border-2", "border-black", "hover:bg-white");
        // Clear display
        document.getElementById("selected-choice-2").textContent = "Please Select a Choice😊";
      } else {
        // Unselect all choices
        document.querySelectorAll('input[name="choice"]').forEach(choice => {
          choice.checked = false;
        });

        // Select the clicked choice
        choiceInput.checked = true;

        // Reset the style of all choice buttons
        document.querySelectorAll(".choice-button").forEach(btn => {
          btn.classList.remove("bg-green-500", "border-solid", "border-2", "border-black", "hover:bg-green-600");
          btn.classList.add("bg-white", "border-solid", "border-2", "border-black", "hover:bg-white");
        });

        button.classList.remove("bg-white", "border-solid", "border-2", "border-black", "hover:bg-white");
        button.classList.add("bg-green-500", "border-solid", "border-2", "border-black", "hover:bg-green-600");

        const choiceText = button.textContent.trim();
        document.getElementById("selected-choice-2").textContent = `You select: ${choiceText}`;
      }
    }
    // Enable the "Vote" button -> if select
    const voteButton = document.getElementById("vote-button");
    voteButton.disabled = !document.querySelector('input[name="choice"]:checked');
  }
};

function confirmChangeVote(choiceId) {
  const confirmation = confirm("Are you sure you want to change your vote?");
  if (confirmation) {
    window.location.href = `{% url 'polls:vote' question.id %}${choiceId}`;
  }
}
