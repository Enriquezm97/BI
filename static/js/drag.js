(function($) {
    $(function() {
        $(".draggable").draggable({
          revert: true,
          helper: 'clone',
          start: function(event, ui) {
            $(this).fadeTo('fast', 0.5);
          },
          stop: function(event, ui) {
            $(this).fadeTo(0, 1);
          }
        });
    
        $("#droppable").autocomplete({
          hoverClass: 'active',
          drop: function(event, ui) {
            this.value += $(ui.draggable).find('select option:selected').text();
          }
        });
      });




})(jQuery);