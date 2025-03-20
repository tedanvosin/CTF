$('#gotoPage').on('change', function() {
  document.location.href =  `/?util=${this.value}`;
});