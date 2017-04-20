function add_ingredient_handler() {
  let new_ingredient_input = $("div > form > p.single-ingredient:first").clone(false);
  for (input of new_ingredient_input.children("input")) {
      input.placeholder = "";
      input.value = "";
  }
  $("div > form > p.single-ingredient:last").after(new_ingredient_input);
}

function add_step_handler() {
    let new_step_input = $("div > form > p.step:first").clone(false);
    for (input of new_step_input.children("input")) {
        input.placeholder = "";
        input.value = "";
    }
    $("div > form > p.step:last").after(new_step_input);
}
