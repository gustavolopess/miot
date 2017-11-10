
function focusFirstSection(elt) {
    $("#second-section").hide();
    $("#third-section").hide();
    $("#first-section").hide().fadeIn("slow");
    changeNavActive(elt);
}

function focusSecondSection(elt) {
    $("#first-section").hide();
    $("#third-section").hide();
    $("#second-section").hide().fadeIn("slow");
    changeNavActive(elt);
}

function focusThirdSection(elt) {
    $("#first-section").hide();
    $("#second-section").hide();
    $("#third-section").hide().fadeIn("slow");
    changeNavActive(elt);
}


function changeNavActive(elt) {
    $(".navbar-nav li").each(function () {
       $(this).removeClass("active");
    });
   $(elt).parent().addClass("active");
}



function hidePage() {
    $('.navbar').hide();
    $('#first-section').hide();
    $('#second-section').hide();
    $('#third-section').hide();
}

function checkSession() {
    var hasSession = false;
    $.ajax({
        async: false,
        url: '/logged/',
        type: 'get',
        success: function () {
            hasSession = true;
        },
        error: function () {
            hasSession = false;
        }
    });
    return hasSession;
}


function splashPage() {
    hidePage();
    document.getElementById("loader").style.display = "block";
    $('body').addClass('animate-bottom');
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    $('.navbar').show();
     if (checkSession()) {
         $('#third-section').fadeIn(1000);
        changeNavActive($('#restricted-area-nav'));
    } else {
         $('#first-section').fadeIn(1000);
    }
    $('body').removeClass('animate-bottom');
}

function getMenuActive(element) {
     $(element)
        .addClass('active')
        .siblings()
        .removeClass('active');
}

function getCollections() {
    var collections;
}

function showCollections() {
    var contentBox = $('#information-segment-content');
    contentBox.empty();
    contentBox.html($('<div class="ui active loader"></div>'));
    $.ajax({
        async: true,
        url: '/api/information/collections',
        type: 'get',
        success: function (data) {
            contentBox.empty();
            var listContainer = $('<div class="ui middle aligned divided list">');
            for (var i in data) {
                // language=HTML
                listContainer.append($('<div class="item">\n' +
                    '    <div class="right floated content">\n' +
                    '      <div class="ui icon buttons">' +
                     '<div class="ui button"><i class="ui icon hourglass half"></i></div>' +
                     '<div class="ui button"><i class="ui icon trash outline"></i></div>' +

                    '</div>\n' +
                    '    </div>\n' +
                    '    <img class="ui avatar image">\n' +
                    '    <div class="content">\n' +
                          data[i]+ '\n' +
                    '    </div>\n' +
                    '  </div>')
                );
            }
            contentBox.append(listContainer);
        },
        error: function (data) {
            alert(JSON.stringify(data));
        }
    });
}


function insertInformation() {
    var contentBox = $('#information-segment-content');
    contentBox.empty();
    contentBox.html($('<div class="ui active loader"></div>'));
    $.ajax({
        async: true,
        url: '/api/information/collections',
        type: 'get',
        success: function (data) {
            contentBox.empty();
            var $selectContainer = $('<select class="selectpicker" data-live-search="true">');
            for (var i in data) {
                // language=HTML
                $selectContainer.append($('<option>'+ data[i] +'</option>'))
            }
            contentBox.append($selectContainer);
            $selectContainer.selectpicker('render');
        },
        error: function (data) {
            alert(JSON.stringify(data));
        }
    });
}



hasSession = false;
$(document).ready(function () {
    var h = $('.request-form').height();
    $('.request-text').css('height', h);
    hidePage();

    var splashTimeout = setTimeout(showPage, 1500);
});


function login() {

    var email = $('input[name=email]').val();
    var password = $('input[name=password]').val();

    hidePage();

    $.ajax({
        url: '/',
        type: 'post',
        dataType: 'html',
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            alert(JSON.stringify(data));

        },
        data: {
            email: email,
            password: password
        }
    });
}
//
//
// function makeRequest(reqFormId, reqWellId, startText) {
//     if (typeof(startText) === "undefined") startText = '\n';
//     else startText = startText + '\n\n';
//
//     var reqWell = $('#' + reqWellId);
//     reqWell.empty();
//
//     var pre = $('<pre></pre>');
//
//     var reqFormFormattedId = '#' + reqFormId;
//     var reqFormInputs = $(reqFormFormattedId + " input");
//     var json = startText + "{\n";
//     reqFormInputs.each(function () {
//         var sub;
//         if ($(this).attr('type') === 'number') sub = $(this).val();
//         else sub = '"' + $(this).val() + '"';
//         json += '\t"' + $(this).attr('name') + '": ' + sub + ",\n";
//     });
//     json = json.substr(0, json.length-2);
//     json += '\n}\n';
//     pre.append(json);
//     reqWell.append(pre);
// }
//
//
// function makeRequestDynamically(reqFormId, dynamicDiv, reqWellId, startText) {
//     if (typeof startText === "undefined") startText = '\n';
//     else startText = startText + '\n\n';
//
//     var reqWell = $('#' + reqWellId);
//     reqWell.empty();
//
//     var pre = $('<pre></pre>');
//
//     var reqFormInputs = $('#' + reqFormId + ' > .request-form > input');
//     var json = startText + "{\n";
//     reqFormInputs.each(function () {
//        var sub;
//        if ($(this).attr('type') === 'number') sub = $(this).val();
//        else sub = '"' + $(this).val() + '"';
//        json += '\t"' + $(this).attr('name') + '": ' + sub + ",\n";
//     });
//
//     var dynamicInputs = $('#' + dynamicDiv + ' input');
//     dynamicInputs.each(function () {
//        // var idx = $(this).attr('aria-label');
//        if ($(this).attr('placeholder') === 'key') {
//             json += '\t"' + $(this).val() + '": ';
//        } else {
//             json += '"' + $(this).val() + '",\n';
//         }
//
//     });
//     json = json.substr(0, json.length-2);
//     json += "\n}\n";
//
//     pre.append(json);
//     reqWell.append(pre);
// }
//
//
// currentInformationIdx = 0;
// function addInformationField() {
//     if (currentInformationIdx == 4) return;
//     var newIdx = currentInformationIdx + 1;
//     var div = $('<div class="form-inline text-center"></div>');
//     var key = $('<input class="form-control" placeholder="key" aria-label="' + newIdx + '" name="key' + newIdx + '">');
//     var value = $('<input class="form-control" placeholder="value" aria-label="' + newIdx + '" name="value' + newIdx + '">');
//     var button = $('<button type="button" class="btn btn-default btn-xs" onclick="addInformationField()">+</button>');
//     div.append(key);
//     div.append(value);
//     div.append(button);
//     $('#informations-container').append(div);
//     $('#informations-container').append('<br>');
//     currentInformationIdx = newIdx;
// }

// function sendRequest(formId, requestPath, requestMethod, ansWellId) {
//     var form = $('#' + formId);
//     var serializedForm = {};
//     form.serializeArray().map(function (item) {
//         serializedForm[item.name] = item.value;
//     });
//     alert(JSON.stringify(serializedForm));
//     $.ajax({
//         url: requestPath,
//         type: requestMethod,
//         contentType: "application/json; charset=utf-8",
//         dataTy$(".navbar-nav a").on("click", function(){
//     alert('OI');
//    $(".navbar-nav li").find(".active").removeClass("active");
//    $(this).parent().addClass("active");
// });pe: "json",
//         data: JSON.stringify(serializedForm),
//         success: function (data) {
//             var ans_well = $('#'+ansWellId);
//             ans_well.empty();
//             ans_well.css('visibility', 'visible');
//             var pre = $('<pre></pre>');
//             pre.append('RESPONSE:\n\n' + JSON.stringify(data, undefined, 2));
//             ans_well.append(pre);
//         },
//         error: function (data) {
//         }
//
//     });
// }

function registerUser() {

}

function registerInformation() {

}

function instanceJSONEditor() {
    var container = document.getElementById('json-editor');
    var options = {
        mode: 'code',
        modes: ['code', 'tree']
    };
    editor = new JSONEditor(container, options);

}


function getJSONFromEditor() {
    var json = editor.get();
    alert(JSON.stringify(json, null, 2));
}


