$(document).ready(function(){

    // When the links are clicked
    $('.filter-link').click(function(){
        
        // First, remove all the active filter tags from the link (if any)
        $('.filter-link').removeClass('filter-active');
        // Then, add the active filter tag for the current link
        $(this).addClass('filter-active');

        const value = $(this).attr('data-filter');
        if (value == "filter-all"){
            $('.imageBox').show('1000');
        }
        else{
            $('.imageBox').not('.'+value).hide('1000')
            $('.imageBox').filter('.'+value).show('1000')
        }

    })
})
