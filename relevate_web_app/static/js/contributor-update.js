/**
	* A javascript for handling dynamic actions with several forms in Relevate.
	* Function that rely on this script include select button and adding academic credentials dynamically

**/
	var academicId;
	var certId;
	var affiliationId;
	var academicTable;
	var certificationTable;
	var affiliationTable;
	var universitySearchUrl;
$(document).ready(function() {
	$(".selected-topics").css('visibility', 'hidden');
    mentorDegreeIds = [];
    console.log("document ready");
    var i = '{{academics_req}}';
    if('{{academics_req}}'){
        console.log('academics');
        var tableId = academicId;
        var res = '{{academics_req}}';
        while(res.length > 0){
            var res = res.split(/[,|]/);
            res[1] = res[1].substring(2);
            res[2] = res[2].substring(2);
                    var academicGrid = "<tr class='rv-contributor-form_box-row acaRow' id=acaProf"+academicId+">" +
                    "<td class='rv-contributor-form_table--item'>" +
                        "<div>" +
                            "<div class='rv-contributor-form_table--item-label'>Program</div>" +
                            "<span class='rv-contributor-form_table--item-content program' value="+res[2]+">" + res[2] + "</span>" +
                        "</div>" +
                    "</td>" +
                    "<td class='rv-contributor-form_table--item'>" +
                        "<div>" +
                            "<div class='rv-contributor-form_table--item-label'>Level of Study</div>" +
                            "<span class='rv-contributor-form_table--item-content degree' value="+res[1]+">" + res[1] + "</span>" +
                        "</div>" +
                    "</td>" +
                    "<td class='rv-contributor-form_table--item'>" +
                        "<div>" +
                            "<div class='rv-contributor-form_table--item-label'>Institution</div>" +
                            "<span class='rv-contributor-form_table--item-content institute' value="+res[0]+">" + res[0] + "</span>" +
                        "</div>" +
                    "</td>" +
                    "<td class='rv-contributor-form_button--container'>" +
                    "<div class='rv-contributor-form_button--group'>" +
                        "<div class='rv-contributor-form_button--group-button'>" +
                            RvButton({
                                variant: 'ghost',
                                color: 'dark',
                                label: 'Edit',
                                icon: 'edit',
                                fluid_width: true,
                                onclick: 'editAcademicProfile(' + tableId + ')'
                            }) +
                          "</div>" +
                          "<div class='rv-contributor-form_button--group-button'>" +
                            RvButton({
                                variant: 'ghost',
                                color: 'dark',
                                label: 'Delete',
                                icon: 'x',
                                fluid_width: true,
                                onclick: 'deleteAcademicProfile(' + tableId + ')'
                            }) +
                          "</div>" +
                    "</div>" +
                    "</td>" +
                "</tr>"
            $("#acaProf").append(academicGrid);
            mentorDegreeIds.push(academicId);
            academicId++;
            updateTablesUpdateInfo(true);
            $("#id_program").val("");
            $("#id_institution").val("");
            $('#id_degree option[value="1"]').prop('selected', true);
            res = res.slice(3);
        }
        $("#list_of_uni").hide()
    }

});
//	var saveInterval = setInterval(saveUnfinished, 15000);
	function addAcademicProfile(){
		/*
			Add academic profile row
		*/
		var academicProgram = $("#id_program").val();
		var degree = $("#id_degree").val();
		var institution = $("#id_institution").val();
		console.log(institution);

		var tableId = academicId;
		if(academicProgram && degree && institution){
			var academicGrid = "<tr class='rv-contributor-form_box-row acaRow' id=acaProf"+academicId+">" +
					"<td class='rv-contributor-form_table--item'>" +
						"<div>" +
							"<div class='rv-contributor-form_table--item-label'>Program</div>" +
							"<span class='rv-contributor-form_table--item-content program' value="+academicProgram+">" + academicProgram + "</span>" +
						"</div>" +
					"</td>" +
					"<td class='rv-contributor-form_table--item'>" +
						"<div>" +
							"<div class='rv-contributor-form_table--item-label'>Level of Study</div>" +
							"<span class='rv-contributor-form_table--item-content degree' value="+degree+">" + degree + "</span>" +
						"</div>" +
					"</td>" +
					"<td class='rv-contributor-form_table--item'>" +
						"<div>" + 
							"<div class='rv-contributor-form_table--item-label'>Institution</div>" +
							"<span class='rv-contributor-form_table--item-content institute' value="+institution+">" + institution + "</span>" +
						"</div>" +
					"</td>" +
					"<td class='rv-contributor-form_button--container'>" +
				   	"<div class='rv-contributor-form_button--group'>" +
				   		"<div class='rv-contributor-form_button--group-button'>" +
						   	RvButton({
						   		variant: 'ghost',
						   		color: 'dark',
						   		label: 'Edit',
						   		icon: 'edit',
						   		fluid_width: true,
						   		onclick: 'editAcademicProfile(' + tableId + ')'
						   	}) +
						  "</div>" +
						  "<div class='rv-contributor-form_button--group-button'>" +
						   	RvButton({
						   		variant: 'ghost',
						   		color: 'dark',
						   		label: 'Delete',
						   		icon: 'x',
						   		fluid_width: true,
						   		onclick: 'deleteAcademicProfile(' + tableId + ')'
						   	}) +
						  "</div>" +
				   	"</div>" +
					"</td>" +
				"</tr>"
			$("#acaProf").append(academicGrid);
			mentorDegreeIds.push(academicId);
			academicId++;
			updateTablesUpdateInfo(true);
			$("#id_program").val("");
			$("#id_institution").val("");
			$('#id_degree option[value="1"]').prop('selected', true);
			$("#list_of_uni").hide()
		}
		else {
		console.log(academicProgram, " acadsdf");
		}
		$("#list_of_uni").hide()
	}
	
	function addCertificate(){
	/*
		Add Certification Row
	*/
		var certificate = $("#id_certification").val();
		var certTableId = certId;
console.log('cert');
		if(certificate){
		    console.log('cert yes');
			var certGrid = "<tr class='rv-contributor-form_box-row certRow' id=addCert"+certTableId+">" +
				"<td class='rv-contributor-form_table--item'>" +
					"<div>" +
						"<div class='rv-contributor-form_table--item-label'>Certification</div>" +
						"<span class='rv-contributor-form_table--item-content certName' value="+certificate+">" + certificate + "</span>" +
					"</div>" +
				"</td>" +
			   "<td class='rv-contributor-form_button--container'>" +
			   	"<div class='rv-contributor-form_button--group'>" +
			   		"<div class='rv-contributor-form_button--group-button'>" +
					   	RvButton({
					   		variant: 'ghost',
					   		color: 'dark',
					   		label: 'Edit',
					   		icon: 'edit',
					   		fluid_width: true,
					   		onclick: 'editCertificate(' + certTableId + ')'
					   	}) +
					  "</div>" +
					  "<div class='rv-contributor-form_button--group-button'>" +
					   	RvButton({
					   		variant: 'ghost',
					   		color: 'dark',
					   		label: 'Delete',
					   		icon: 'x',
					   		fluid_width: true,
					   		onclick: 'deleteCertificate(' + certTableId + ')'
					   	}) +
					  "</div>" +
				  "</div>" +
				"</td>" +
			"</tr>"
			$("#addCert").append(certGrid);
			certId++;
            console.log('cert end');
			updateTablesUpdateInfo(false);
			$("#id_certification").val("");
		}
		$("#list_of_uni").hide()
	}

	function addAffiliation(){
	/*
		Add Attribute Row
	*/
		var affiliation = $("#id_organizational_affiliation").val();
		var affiliationTableId = affiliationId;

		if(affiliation){
			var affiliationGrid = "<tr class='rv-contributor-form_box-row affiliationRow' id=addAffiliation"+affiliationTableId+">" +
				"<td class='rv-contributor-form_table--item'>" +
					"<div>" +
						"<div class='rv-contributor-form_table--item-label'>Affiliation</div>" +
						"<span class='rv-contributor-form_table--item-content affilName' value="+affiliation+">" + affiliation + "</span>" +
					"</div>" +
				"</td>" +
			   "<td class='rv-contributor-form_button--container'>" +
			   	"<div class='rv-contributor-form_button--group'>" +
			   		"<div class='rv-contributor-form_button--group-button'>" +
					   	RvButton({
					   		variant: 'ghost',
					   		color: 'dark',
					   		label: 'Edit',
					   		icon: 'edit',
					   		fluid_width: true,
					   		onclick: 'editAffiliation(' + affiliationTableId + ')'
					   	}) +
					  "</div>" +
					  "<div class='rv-contributor-form_button--group-button'>" +
					   	RvButton({
					   		variant: 'ghost',
					   		color: 'dark',
					   		label: 'Delete',
					   		icon: 'x',
					   		fluid_width: true,
					   		onclick: 'deleteAffiliation(' + affiliationTableId + ')'
					   	}) +
					  "</div>" +
				  "</div>" +
				"</td>" +
			"</tr>"
			$("#addAffiliation").append(affiliationGrid);
			affiliationId++;

			updateTablesUpdateInfo(false);
			$("#id_organizational_affiliation").val("");
		}
		$("#list_of_uni").hide()
	}

	function replaceWithTextInput (parent, label, placeholder) {
		var newInput = document.createElement('div')
		newInput.innerHTML = RvTextInput({
			label: label,
			value: parent.firstChild.textContent,
			placeholder: placeholder
		})
		parent.replaceChild(newInput, parent.firstChild)
	}

	function replaceWithSelect (selectRow, parent, label, placeholder) {
		var options = []
		var items = selectRow.getElementsByTagName('LI')

		for (var i = 0; i < items.length; i++) {
			var option = items[i]
			if (option.getAttribute('class') !== 'rv-select_option--placeholder') {
				options.push(option.textContent)
			}
		}

		var current = parent.firstChild

		var edit = document.createElement('div')
		edit.innerHTML = RvSelect({
			label: label,
			placeholder: placeholder,
			value: current.textContent,
			options: options,
			editable: true
		})

		parent.replaceChild(edit, current)	
	}

	function hideLabels (row) {
		var labels = row.getElementsByClassName('rv-contributor-form_table--item-label')
		for (var i = 0; i < labels.length; i++) {
			labels[i].setAttribute('style', 'display: none')
		}
	}

	function showLabels (row) {
		var labels = row.getElementsByClassName('rv-contributor-form_table--item-label')
		for (var i = 0; i < labels.length; i++) {
			labels[i].setAttribute('style', 'display: block')
		}
	}

	function convertEditToSaveButton (id, row, onclick) {
		var buttonGroup = row.getElementsByClassName('rv-contributor-form_button--group-button')[0]
		var editButton = buttonGroup.firstElementChild

		replaceButton(editButton, 'Save', 'primary', 'save', onclick)
	}

	function convertSaveToEditButton (id, row, onclick) {
		var buttonGroup = row.getElementsByClassName('rv-contributor-form_button--group-button')[0]
		var editButton = buttonGroup.firstElementChild

		replaceButton(editButton, 'Edit', 'dark', 'edit', onclick)
	}

	function replaceButton(oldButton, label, color, icon, onclick) {
		var parent = oldButton.parentElement
		var newButton = document.createElement('div')
		newButton.innerHTML = RvButton({
			label: label,
			type: 'button',
			variant: 'ghost',
			color: color,
			icon: icon,
			fluid_width: true,
			onclick: onclick
		})

		parent.replaceChild(newButton.firstElementChild, oldButton)
		
		// Focus the replaced button for keyboard accessibility
		var buttons = parent.querySelectorAll('button')
		for (var i = 0; i < buttons.length; i++) {
			var button = buttons[i]
			if (button.textContent.trim() === label) {
				button.focus()
			}
		}
	}

	function editAcademicProfile (id) {
		var row = document.getElementById('acaProf' + id)
		var rowItems = row.getElementsByClassName('rv-contributor-form_table--item-content')

		hideLabels(row)

		var program = rowItems[0]
		replaceWithTextInput(program, 'Program', 'Ex. Psychology')

		replaceWithSelect(
			document.getElementById('acaProfCreate'), 
			rowItems[1], 
			'Level of Study',
			'Enter your level of study'
		)

		var institution = rowItems[2]
		replaceWithTextInput(institution, 'Institution', 'Ex. Kansas State')

		convertEditToSaveButton(id, row, 'saveAcademicProfileEdit(' + id + ')')
	}

	function saveAcademicProfileEdit (id) {
		var row = document.getElementById('acaProf' + id)
		var rowItems = row.getElementsByClassName('rv-contributor-form_table--item-content')

		showLabels(row)

		var program = rowItems[0].firstChild
		program.innerHTML = program.getElementsByTagName('INPUT')[0].value

		var study = rowItems[1].firstChild
		study.innerHTML = study.getElementsByTagName('INPUT')[0].value

		var institution = rowItems[2].firstChild
		institution.innerHTML = institution.getElementsByTagName('INPUT')[0].value

		convertSaveToEditButton(id, row, 'editAcademicProfile(' + id + ')')
	}

	function deleteAcademicProfile (id) {
		/*
			Delete Academic Profile Row
		*/
		$("#acaProf"+id).remove();
		updateTablesUpdateInfo(true);

		if (mentorDegreeIds.includes(id))
		{
			var index = mentorDegreeIds.indexOf(id);
			mentorDegreeIds.splice(index, 1);

			if (mentorDegreeIds.length == 0 && !($("#adviser-div").hasClass("uk-hidden")))
			{
				mentorNeeded = false;
				$('#id_adviser').val("");
				$("#adviser-div").addClass('uk-hidden');
			}

		}
		$("#list_of_uni").hide()
	}

	function editCertificate (id) {
		var row = document.getElementById('addCert' + id)
		var rowItems = row.getElementsByClassName('rv-contributor-form_table--item-content')

		hideLabels(row)

		var certificate = rowItems[0]
		replaceWithTextInput(certificate, 'Certifications', 'Enter a certification')

		convertEditToSaveButton(id, row, 'saveCertificateEdit(' + id + ')')
	}

	function saveCertificateEdit (id) {
		var row = document.getElementById('addCert' + id)
		var rowItems = row.getElementsByClassName('rv-contributor-form_table--item-content')

		showLabels(row)

		var certificate = rowItems[0].firstChild
		certificate.innerHTML = certificate.getElementsByTagName('INPUT')[0].value

		convertSaveToEditButton(id, row, 'editCertificate(' + id + ')')
	}


	function deleteCertificate (id) {
	/*
		Delete Certification Row
	*/
		$("#addCert"+id).remove();
		updateTablesUpdateInfo(false);
		$("#list_of_uni").hide()
	}

	function editAffiliation (id) {
		var row = document.getElementById('addAffiliation' + id)
		var rowItems = row.getElementsByClassName('rv-contributor-form_table--item')

		hideLabels(row)

		replaceWithSelect(
			document.getElementById('affiliationCreate'), 
			rowItems[0], 
			'Organizational Affiliations',
			'Ex. NCFR'
		)

		convertEditToSaveButton(id, row, 'saveAffiliationEdit(' + id + ')')
	}

	function saveAffiliationEdit (id) {
		var row = document.getElementById('addAffiliation' + id)
		var rowItems = row.getElementsByClassName('rv-contributor-form_table--item-content')

		showLabels(row)

		var affiliation = rowItems[0].firstChild
		affiliation.innerHTML = affiliation.getElementsByTagName('INPUT')[0].value

		convertSaveToEditButton(id, row, 'editAffiliation(' + id + ')')
	}

	function deleteAffiliation(id){
	/*
		Delete Attribute Row
	*/
		$("#addAffiliation"+id).remove();
		updateTablesUpdateInfo(false);
		$("#list_of_uni").hide()
	}


//    function saveUnfinished() {
//        var d = new Date();
//        document.getElementById("demo").innerHTML = d.toLocaleTimeString();
//    }

	function updateTablesUpdateInfo(is_academic_update){
	/*
		Updates Table Information dynamically.
		Basically each academic information entered by user in each column is converted into one string
		divided by escape strings (|%$) then stored in an array.
		See the variable sudoDic and newSudoDic below.
	*/
		var makeSureString = '%';
		var sudoDic;
		var newSudoDic;
		if(is_academic_update == true){

			var academicTableName = '#acaProf > tbody  > tr.acaRow';

			 academicTable = [];

			$(academicTableName).each(function() {
			console.log('acalog');
				$this = $(this)
				var dicObj = {};
				instituteVal = $this.find('span.institute').html();
				degreeVal = $this.find('span.degree').html();
				programVal = $this.find('span.program').html()
				sudoDic = instituteVal + "|%$" + degreeVal + '|%$' + programVal;
				newSudoDic = sudoDic.concat(makeSureString);
				academicTable.push(newSudoDic)
			});
			var acLength = academicTable.length;
			if(acLength > 0){
				var lastElement = academicTable[acLength - 1];
				var newLastElement = lastElement.substring(0, lastElement.length -1);
				academicTable[acLength - 1] = newLastElement;
			}

		}else{
			var certTableName = '#addCert > tbody  > tr.certRow';
			certificationTable = [];
			 $(certTableName).each(function() {
				$this = $(this)
				certificate = $this.find('span.certName').html();
				sudoDic = certificate;
				newSudoDic = sudoDic.concat(makeSureString);
				console.log(newSudoDic);
				certificationTable.push(newSudoDic);
			 });
			 var acLength = certificationTable.length;
			 if(acLength > 0){
				 var lastElement = certificationTable[acLength - 1];
				 var newLastElement = lastElement.substring(0, lastElement.length -1);
				 certificationTable[acLength - 1] = newLastElement;
			 }
			 var affiliationTableName = '#addAffiliation > tbody > tr.affiliationRow';
			 affiliationTable = [];
			  $(affiliationTableName).each(function() {
			    $this = $(this)
			    affiliation = $this.find('span.affilName').html();
			    sudoDicAffil = affiliation;
			    newSudoDicAffil = sudoDicAffil.concat(makeSureString);
			    affiliationTable.push(newSudoDicAffil);
			 });
             var afLength = affiliationTable.length;
             if(afLength > 0){
                 var lastElementAffil = affiliationTable[afLength - 1];
                 var newLastElementAffil = lastElementAffil.substring(0, lastElementAffil.length -1);
                 affiliationTable[afLength - 1] = newLastElementAffil;
             }
		 }
		 $("#hiddenAcaTable").val(academicTable);
		 console.log($("#hiddenAcaTable").val());
		 $("#hiddenCertTable").val(certificationTable);
		 console.log($("#hiddenCertTable").val());
		 console.log(certificationTable);
		 $("#hiddenAffilTable").val(affiliationTable);

		$("#list_of_uni").hide()
	}

	function switchTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


