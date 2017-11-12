$(function(){
  
  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };
  var colors = ['#b7d3f2', '#afafdc', '#8a84e2', '#84afe6', '#79beee'];
  $('.item').each(function(index,el){
    var randomColorIndex = getRandomInt(0,colors.length-1);
    $(el).css('background-color',colors[randomColorIndex]);
  });
});