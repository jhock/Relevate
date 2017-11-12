//This is the configuration for the basic or default text entry form, mainly used to keep form entry consistent.
CKEDITOR.editorConfig = function( config ) {
    config.toolbarGroups = [
        { name: 'basicstyles', groups: [ 'basicstyles'] },
    ];
    config.removeButtons = 'Superscript,Subscript,Strike';
};