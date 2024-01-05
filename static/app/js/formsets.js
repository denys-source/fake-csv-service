$(document).ready(function() {
  $(".add-form").on("click", function() {
    let prefix = $(this).closest(".formset").data("formset-prefix");
    let form_id = $(`#id_${prefix}-TOTAL_FORMS`).val();

    let empty_form = $(`.${prefix}-empty-form`).clone();
    $(this).before(empty_form.html().replace(/__prefix__/g, form_id));

    $(`#id_${prefix}-TOTAL_FORMS`).val(parseInt(form_id) + 1);
  });

  $(".formset").on("click", ".delete-form", function() {
    let prefix = $(this).closest(".formset").data("formset-prefix");

    $(this).closest(".column-form").remove();

    let form_id = $(`#id_${prefix}-TOTAL_FORMS`).val();
    $(`#id_${prefix}-TOTAL_FORMS`).val(parseInt(form_id) - 1);
  });

  $("fieldset.collapsable legend").click(function() {
    $(this).parent().toggleClass("active");
  });
});
