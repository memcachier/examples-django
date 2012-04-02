$(function() {
  $("input[data-compute]").live("click", function() {
    var answer = $("#answer");
    answer.html("Working ...");
    $.get(
      "/compute?a=" + $("#a").val() + "&b=" + $("#b").val() + "&op=" + $("#op").val(),
      function(data) {
        answer.html(data);
      }
    );
  });
});