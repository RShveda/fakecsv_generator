var path = window.location.pathname;

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
    $('#'+id).html("download");
    $('#'+id).toggleClass('disabled btn-outline-warning', false);
    $('#'+id).toggleClass('btn-outline-success', true);
    const status = res.status;
    console.log(res.status)
    if (status === 'uploaded') return false;
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