    // popovers initialization - on hover
    $('[data-toggle="popover-hover"]').popover({
        html: true,
        trigger: 'hover',
        placement: 'right',
        content: function () { return '<img src="' + $(this).data('img') + '" />'; }
      });