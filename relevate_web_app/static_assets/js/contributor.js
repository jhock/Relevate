/**
	* A javascript for handling dynamic actions with several forms in Relevate.
	* Function that rely on this script include select button and adding academic credentials dynamically

**/

$(document).ready(function() {
	$(".selected-topics").css('visibility', 'hidden');
    mentorDegreeIds = [];

});
	var academicId;
	var certId;
	var affiliationId;
	var academicTable;
	var certificationTable;
	var affiliationTable;
	var universitySearchUrl;

	function addAcademicProfile(){
		/*
			Add academic profile row
		*/
		var academicProgram = $("#id_program").val();
		console.log(academicProgram, " acad");
		var degreeVal = $("#id_degree option:selected").val();
		console.log(degreeVal, " ");
		var institution = $("#id_institution").val();
		console.log(institution, " ");
		var degree = $("#id_degree option:selected").text();
		var tableId = academicId;
		if(academicProgram && degreeVal && institution){
			var academicGrid = "<tr class='acaRow' id=acaProf"+academicId+">" +
					"<td>" +
						"<div  class='uk-form-controls'><span class='program' value="+academicProgram+">" + academicProgram +
						"</span></div>" +
					"</td>" +
					"<td>" +
						"<div  class='uk-form-controls'><span class='degree' value="+degreeVal+">" + degree +
						"</span></div>" +
					"</td>" +
					"<td>" +
						"<div value="+institution+" class='uk-form-controls'><span class='institute' value="+institution+">" + institution +
						"</span></div>" +
					"</td>" +
				   "<td>" +
						"<button type='button' class='uk-button uk-button-orange degree-delete-btn' onclick='deleteAcademicProfile("+tableId+")'>delete</button> "+
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
		$("#list_of_uni").hide()
	}
	
	function addCertificate(){
	/*
		Add Certification Row
	*/
		var certificate = $("#id_certification").val();
		var certTableId = certId;
		if(certificate){
			var certGrid = "<tr class='certRow' id=addCert"+certTableId+">" +
				"<td>" +
					"<div class='uk-form-controls'><span class='certName' value="+certificate+">" + certificate +
					"</span></div>" +
				"</td>" +
			   "<td>" +
					"<button type='button' class='uk-button uk-button-orange' onclick='deleteCertificate("+certTableId+")'>delete</button> "+
				"</td>" +
			"</tr>"
			$("#addCert").append(certGrid);
			certId++;

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
			var affiliationGrid = "<tr class='affiliationRow' id=addAffiliation"+affiliationTableId+">" +
				"<td>" +
					"<div class='uk-form-controls'><span class='affiliationName' value="+affiliation+">" + affiliation +
					"</span></div>" +
				"</td>" +
			   "<td>" +
					"<button type='button' class='uk-button uk-button-orange' onclick='deleteAffiliation("+affiliationTableId+")'>delete</button> "+
				"</td>" +
			"</tr>"
			$("#addAffiliation").append(affiliationGrid);
			affiliationId++;

			updateTablesUpdateInfo(false);
			$("#id_organizational_affiliation").val("");
		}
		$("#list_of_uni").hide()
	}

	function deleteAcademicProfile(id)
	{
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


	function deleteCertificate(id){
	/*
		Delete Certification Row
	*/
		$("#addCert"+id).remove();
		updateTablesUpdateInfo(false);
		$("#list_of_uni").hide()
	}

	function deleteAffiliation(id){
	/*
		Delete Attribute Row
	*/
		$("#addAffiliation"+id).remove();
		updateTablesUpdateInfo(false);
		$("#list_of_uni").hide()
	}

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
			    affiliation = $this.find('span.affiliationName').html();
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
		 $("#hiddenCertTable").val(certificationTable);
		 $("#hiddenAffilTable").val(affiliationTable);

		$("#list_of_uni").hide()
	}


