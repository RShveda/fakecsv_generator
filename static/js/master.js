console.log("js loaded")

var path = window.location.pathname;
console.log(path)

if (path == "/schemas/datasets/") {
    var datasets = $(".btn-status")
    console.log(path)
    for (var i = 0; i < datasets.length; i++){
        getStatus(datasets.eq(i).attr("id"))
    }
}

function getStatus(id) {
  $.ajax({
    url: `/schemas/datasets/${id}/`,
    method: 'GET'
  })
  .done((res) => {
    console.log(id)
    $('#'+id).html("Ready");
    $('#'+id).toggleClass('disabled btn-outline-warning', false);
    $('#'+id).toggleClass('btn-outline-success', true);
    const status = res.status;
    const url = res.url;
    $('#'+id).attr("href", url);
    console.log(res.status)
    if (status === 'ready') return false;
    $('#'+id).html(status);
    $('#'+id).toggleClass('disabled btn-outline-warning', true);
    $('#'+id).toggleClass('btn-outline-success', false);
    setTimeout(function() {
      getStatus(id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });

}


// when loaded column edit page with following pattern: "schemas/columns/{{column.name}}/edit"
if (path.startsWith("/schemas/columns/") == true && path.endsWith("/edit") == true) {
    switchRanges()
}

function switchRanges() {
    console.log("switchResult executing")
    var id = $("#data-type-input option:selected")
    var minRange = $("#min-range-input")
    var maxRange = $("#max-range-input")
    if (id.text() === "integer" || id.text() === "text"){
        minRange.prop("disabled", false)
        maxRange.prop("disabled", false)
    }
    else{
        minRange.prop("disabled", true)
        maxRange.prop("disabled", true)
    }
}