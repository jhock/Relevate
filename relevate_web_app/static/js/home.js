$(function(){

  // We're going to go with a white background on the cards
  // for a cleaner feel. But we'll change the heading colors
  // (possibly random as well) so we'll need this js moving 
  // forward. We'll just repurpose it to apply to the card
  // attributes we want to colorize later on. I've commented
  // it out for now.
  
  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  var colors = [
    '#6E307B', 
    '#6F9348', 
    '#FF8100', 
    '#0F3765', 
    '#B50D22', 
    '#4A4A4A', 
    '#62BAB1',
    '#548F9E'
  ];
  
  $('.rv-content-card').each(function(index, card){
    var randomColorIndex = getRandomInt(0,colors.length-1);

    var heading = $(card).find('.rv-content-card_heading')[0];
    $(heading).css('color', colors[randomColorIndex]);

    var rule = $(card).find('.rv-content-card_contributor-rule')[0];
    $(rule).css('color', colors[randomColorIndex]);
  });

  $('.cloud').each(function(index, el) {
    el.classList.add('cloud-animate')
  });
});