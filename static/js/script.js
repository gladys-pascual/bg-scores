$(document).ready(function () {
  $(".dropdown-trigger").dropdown({ coverTrigger: false, hover: true });
  $(".sidenav").sidenav({ edge: "right" });
  $(".datepicker").datepicker({
    format: "dd mmm yyyy",
    yearRange: 1,
    showClearBtn: true,
    i18n: {
      done: "Select",
    },
  });
  $("select").formSelect();
  validateMaterializeSelect();
  function validateMaterializeSelect() {
    let classValid = {
      "border-bottom": "1px solid #4caf50",
      "box-shadow": "0 1px 0 0 #4caf50",
    };
    let classInvalid = {
      "border-bottom": "1px solid #f44336",
      "box-shadow": "0 1px 0 0 #f44336",
    };
    if ($("select.validate").prop("required")) {
      $("select.validate").css({
        display: "block",
        height: "0",
        padding: "0",
        width: "0",
        position: "absolute",
      });
    }
    $(".select-wrapper input.select-dropdown")
      .on("focusin", function () {
        $(this)
          .parent(".select-wrapper")
          .on("change", function () {
            if (
              $(this)
                .children("ul")
                .children("li.selected:not(.disabled)")
                .on("click", function () {})
            ) {
              $(this).children("input").css(classValid);
            }
          });
      })
      .on("click", function () {
        if (
          $(this)
            .parent(".select-wrapper")
            .children("ul")
            .children("li.selected:not(.disabled)")
            .css("background-color") === "rgba(0, 0, 0, 0.03)"
        ) {
          $(this).parent(".select-wrapper").children("input").css(classValid);
        } else {
          $(".select-wrapper input.select-dropdown").on(
            "focusout",
            function () {
              if (
                $(this)
                  .parent(".select-wrapper")
                  .children("select")
                  .prop("required")
              ) {
                if (
                  $(this).css("border-bottom") != "1px solid rgb(76, 175, 80)"
                ) {
                  $(this)
                    .parent(".select-wrapper")
                    .children("input")
                    .css(classInvalid);
                }
              }
            }
          );
        }
      });
  }

  $("#players li").on("click", function () {
    const selectedPlayers = [
      ...document.querySelectorAll("#players li.selected "),
    ].map((el) => el.textContent);
    $("#selected-players").empty();

    selectedPlayers.forEach((player) =>
      $("#selected-players").append(`
        <div class="col s6 offset-m2 player-name-wrapper">
	        <p class="player-name"><i class="far fa-user prefix"></i>${player}</p>
				</div>
        <div class="input-field col s6 m2 score">
          <input
						id="score"
						name="score"
						min="0"
						type="number" 
						class="validate" 
						required
						>
					<label for="score">Score</label>	
          </div>
        </div>
        `)
    );
  });

  $("#edit-players li").on("click", function () {
    const editSelectedPlayers = [
      ...document.querySelectorAll("#edit-players li.selected "),
    ].map((el) => el.textContent);
    $("#edit-selected-players").empty();

    editSelectedPlayers.forEach((player) =>
      $("#edit-selected-players").append(`
        <div class="col s6 offset-m2 player-name-wrapper">
	        <p class="player-name"><i class="far fa-user prefix"></i>${player}</p>
				</div>
        <div class="input-field col s6 m2 score">
          <input
						id="edit_score"
						name="edit_score"
						min="0"
						type="number" 
						class="validate" 
						required
						>
					<label for="edit_score">Score</label>	
          </div>
        </div>
        `)
    );
  });
});
