const loadPlayersUrl =
  "https://n6mr2kuwhbpgjzkqdh4zog4uny0qmcro.lambda-url.eu-central-1.on.aws/";
const saveRatingUrl =
  "https://cyeb2c2k6rph5ejbwhyhyndiay0itefp.lambda-url.eu-central-1.on.aws/";
const main = async () => {
  let players = [];
  let winner;
  let loser;
  let selectionMode = "winner";

  const loadPlayers = async () => {
    const players = await fetch(loadPlayersUrl);
    const data = await players.json();
    return data;
  };

  players = await loadPlayers();

  const playerContainer = document.getElementById("playerContainer");
  players.forEach((element) => {
    const playerElement = document.createElement("div");
    playerElement.classList.add("player");
    playerElement.id = element.name + "-container";

    const playerName = document.createElement("h2");
    playerName.textContent = element.name;

    const playerRating = document.createElement("p");
    playerRating.id = element.name + "-rating";
    playerRating.textContent = element.rating;

    const playerRatingGain = document.createElement("span");
    playerRatingGain.classList.add("rating-difference");
    playerRatingGain.classList.add("hidden");
    playerRating.appendChild(playerRatingGain);

    playerElement.appendChild(playerName);
    playerElement.appendChild(playerRating);

    playerElement.onclick = (ev) => {
      if (selectionMode === "winner") {
        resetWinner();
        if (loser === element.name) {
          resetLoser();
        }

        winner = element.name;
        playerElement.classList.add("winner");
        selectionMode = "loser";
      } else {
        resetLoser();
        if (winner === element.name) {
          resetWinner();
        }

        loser = element.name;
        playerElement.classList.add("loser");
        selectionMode = "winner";
      }
    };

    playerContainer.appendChild(playerElement);
  });

  const resetWinner = () => {
    winner = undefined;

    document
      .getElementById("playerContainer")
      .childNodes.forEach((playerElement) => {
        playerElement.classList.remove("winner");
      });
  };

  const resetLoser = () => {
    loser = undefined;

    document
      .getElementById("playerContainer")
      .childNodes.forEach((playerElement) => {
        playerElement.classList.remove("loser");
      });
  };

  const reset = () => {
    resetWinner();
    resetLoser();
  };

  const submit = async () => {
    if (!winner || !loser) return;

    console.log("submitted");

    const response = await fetch(saveRatingUrl, {
      method: "POST",
      body: JSON.stringify({ player1: winner, player2: loser }),
    });
    const data = await response.json();
    updateRating(data[0], data[1]);
    reset();
  };

  document.body.onkeypress = (ev) => {
    if (ev.key === "Enter") {
      submit();
    }
  };

  document.getElementById("submit").onclick = (ev) => {
    submit();
  };
  const titles = [
    "SkillScore Pro",
    "RankMaster 9000",
    "Competitive Skill Index",
    "GameRank Evaluator",
    "VictoryMetrics Hub",
    "SkillForge Analytics",
    "GameMastery Insights",
    "StrategiRater Elite",
    "ProSkill Analyzer",
    "VictoryVector Pro",
  ];

  const randomIndex = Math.floor(Math.random() * titles.length);
  const randomTitle = titles[randomIndex];

  document.title = randomTitle;
  document.getElementById("title").textContent = randomTitle;

  function updateRating(winner, loser) {
    animateRatingDifference(winner, true);
    animateRatingDifference(loser, false);
  }

  const animateRatingDifference = (player, isWinner) => {
    let oldRating = players.find((p) => p.name === player.name).rating;
    let ratingDifference = player.rating - oldRating;

    const totalAnimationDuration = 2000;
    const animationDurationPerFrame = totalAnimationDuration / Math.abs(ratingDifference);
    players = players.map((p) => (p.name === player.name ? player : p));
    const playerRating = document.getElementById(player.name + "-rating");

    const ratingEle =
      playerRating.getElementsByClassName("rating-difference")[0];
    ratingEle.textContent = (isWinner ? "+" : "") + ratingDifference;
    ratingEle.classList.add(isWinner ? "text-green" : "text-red");
    ratingEle.classList.remove("hidden");

    const makeRatingCountdown = () => {
      const direction = isWinner ? 1 : -1;
      ratingDifference -= direction;
      ratingEle.textContent = (isWinner ? "+" : "") + ratingDifference;
      oldRating += direction;

      // Update the content directly without removing children
      playerRating.childNodes[0].nodeValue = oldRating;

      if (ratingDifference !== 0) {
        setTimeout(makeRatingCountdown, animationDurationPerFrame);
      } else {
        ratingEle.classList.remove("text-green");
        ratingEle.classList.remove("text-red");
        ratingEle.classList.add("hidden");
      }
    };

    makeRatingCountdown();
  };
};

main();
