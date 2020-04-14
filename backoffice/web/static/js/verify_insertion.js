$(function () {
    $("#addButton").click(handleSubmit);
});

function handleSubmit(submitEvent){
    const fields = $("#insertionForm").serializeArray();
    $.post("/add_article", fields, checkInsertion);
    submitEvent.preventDefault();
    $("#addButton").html('<img src="/img/ajax-loader.gif" />');
}

function checkInsertion(data){
    $("#addButton").html("Ajouter");
    $("#insertionModal").modal("show");
}