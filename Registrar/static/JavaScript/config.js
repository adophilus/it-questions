$(document).ready(function () {
    function deleteGrade (event) {
        document.getElementById("gradeSpace").removeChild(event.target.parentNode);
    }

    function deleteDepartment (event) {
        document.getElementById("schoolDepartmentsSpace").removeChild(event.target.parentNode);
    }

    document.querySelectorAll("button[delete-grade]").forEach(function (element) {
        element.onclick = function (event) {
            deleteGrade(event);
        }
    });
    
    document.querySelectorAll("button[delete-department]").forEach(function (element) {
        element.onclick = function (event) {
            deleteDepartment(event);
        }
    });
    
    $("#configurationForm").on("submit", function (e) {
        e.preventDefault();
    });
    
    $("#addGrade").click(function () {
        var row = document.createElement("div");
        row.setAttribute("class", "row");
        row.setAttribute("grade", "");
        row.style = "margin-top: 5px; margin-bottom: 5px";
        
        var activeDiv = document.createElement("div");
        activeDiv.setAttribute("class", "col col col-xl-1 col-lg-1 col-md-1 col-sm-1");
        
        var active = document.createElement("input");
        active.setAttribute("type", "checkbox");
        
        activeDiv.appendChild(active);
        
        
        var gradeDiv = document.createElement("div");
        gradeDiv.setAttribute("class", "col col col-xl-1 col-lg-1 col-md-1 col-sm-1");
        gradeDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var grade = document.createElement("input");
        grade.setAttribute("type", "text");
        grade.setAttribute("class", "form-control");
        
        gradeDiv.appendChild(grade);
        
        
        var lowerLimitDiv = document.createElement("div");
        lowerLimitDiv.setAttribute("class", "col col-xl-2 col-lg-2 col-md-2 col-sm-2");
        lowerLimitDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var lowerLimit = document.createElement("input");
        lowerLimit.setAttribute("type", "number");
        lowerLimit.setAttribute("class", "form-control");
        
        lowerLimitDiv.appendChild(lowerLimit);
        
        
        var upperLimitDiv = document.createElement("div");
        upperLimitDiv.setAttribute("class", "col col-xl-2 col-lg-2 col-md-2 col-sm-2");
        upperLimitDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var upperLimit = document.createElement("input");
        upperLimit.setAttribute("type", "number");
        upperLimit.setAttribute("class", "form-control");
        
        upperLimitDiv.appendChild(upperLimit);
        
        
        var remarkDiv = document.createElement("div");
        remarkDiv.setAttribute("class", "col col-xl-2 col-lg-2 col-md-2 col-sm-2");
        remarkDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var remark = document.createElement("input");
        remark.setAttribute("type", "text");
        remark.setAttribute("class", "form-control");
        
        remarkDiv.appendChild(remark);
        
        
        var displayTextDiv = document.createElement("div");
        displayTextDiv.setAttribute("class", "col col-xl-2 col-lg-2 col-md-3 col-sm-2");
        displayTextDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var displayText = document.createElement("input");
        displayText.setAttribute("type", "text");
        displayText.setAttribute("class", "form-control");
        
        displayTextDiv.appendChild(displayText);
        
        
        var overallRemarkDiv = document.createElement("div");
        overallRemarkDiv.setAttribute("class", "col col-xl-3 col-lg-3 col-md-3 col-sm-2");
        overallRemarkDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var overallRemark = document.createElement("input");
        overallRemark.setAttribute("type", "text");
        overallRemark.setAttribute("class", "form-control");
        
        overallRemarkDiv.appendChild(overallRemark);
        
        var deleteGradeBtn = document.createElement("button");
        deleteGradeBtn.setAttribute("type", "button");
        deleteGradeBtn.setAttribute("class", "btn");
        deleteGradeBtn.innerHTML = "&times;"
        deleteGradeBtn.onclick = function (event) {
            deleteGrade(event);
        }
        
        row.appendChild(activeDiv);
        row.appendChild(gradeDiv);
        row.appendChild(lowerLimitDiv);
        row.appendChild(upperLimitDiv);
        row.appendChild(remarkDiv);
        row.appendChild(displayTextDiv);
        row.appendChild(overallRemarkDiv);
        row.appendChild(deleteGradeBtn);

        document.getElementById("gradeSpace").appendChild(row);
    });
    
    $("#addDepartment").click(function () {
        var row = document.createElement("div");
        row.setAttribute("class", "row");
        row.setAttribute("grade", "");
        row.style = "margin-top: 5px; margin-bottom: 5px";
        
        var activeDiv = document.createElement("div");
        activeDiv.setAttribute("class", "col col col-xl-1 col-lg-1 col-md-1 col-sm-1");
        
        var active = document.createElement("input");
        active.setAttribute("type", "checkbox");
        
        activeDiv.appendChild(active);
        
        
        var departmentDiv = document.createElement("div");
        departmentDiv.setAttribute("class", "col col-xl-3 col-lg-3 col-md-3 col-sm-3");
        departmentDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var department = document.createElement("input");
        department.setAttribute("type", "text");
        department.setAttribute("class", "form-control");
        
        departmentDiv.appendChild(department);


        var descriptionDiv = document.createElement("div");
        descriptionDiv.setAttribute("class", "col col-xl-4 col-lg-4 col-md-4 col-sm-4");
        descriptionDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var description = document.createElement("input");
        description.setAttribute("type", "text");
        description.setAttribute("class", "form-control");
        
        descriptionDiv.appendChild(description);


        var displayNameDiv = document.createElement("div");
        displayNameDiv.setAttribute("class", "col col-xl-2 col-lg-2 col-md-3 col-sm-2");
        displayNameDiv.style = "margin-left: -20px; margin-right: -10px";
        
        var displayName = document.createElement("input");
        displayName.setAttribute("type", "text");
        displayName.setAttribute("class", "form-control");
        
        displayNameDiv.appendChild(displayName);
        

        var deleteDepartmentBtn = document.createElement("button");
        deleteDepartmentBtn.setAttribute("type", "button");
        deleteDepartmentBtn.setAttribute("class", "btn");
        deleteDepartmentBtn.innerHTML = "&times;"
        deleteDepartmentBtn.onclick = function (event) {
            deleteDepartment(event);
        }
        
        row.appendChild(activeDiv);
        row.appendChild(departmentDiv);
        row.appendChild(descriptionDiv);
        row.appendChild(displayNameDiv);
        row.appendChild(deleteDepartmentBtn);

        document.getElementById("schoolDepartmentsSpace").appendChild(row);
    });
});