
$(document).ready(function(){

    let $active = $('.question').first()
    $active.show()
    let $displayMessage = NaN
    let score = []

    const $correctAnswer = $('#correct-answer')
    const $wrongAnswer = $('#wrong-answer')
    const $helpText = $(".hint-message")

    const messageSpeed = 750
    const messagePauseTime = 3000


    $("form").submit(function(event){
        event.preventDefault()
        let question_id = $(this).attr("data-question-id")
        let form_data = new FormData(this)
        let option_selected = form_data.get("question")


        $.ajax({
            url: "/grade_question",
            type: "get",
            data: {
                question_id: question_id,
                answer_selected: option_selected
            },
            dataType: 'json',
            success: (function (data, status, xhr) {
                score.push(data.correct)

                $active.hide()

                // figure out which message to show and show it
                if (data.correct === false) {
                    $displayMessage = $wrongAnswer
                } else {
                    $displayMessage = $correctAnswer
                }
                $helpText.html(data.help_text)

                $displayMessage.slideDown(messageSpeed)
                setTimeout(() => {
                    $displayMessage.slideUp(messageSpeed)
                }, messagePauseTime)

                // display next question
                setTimeout(() => {
                    $active = $active.next('form')
                    if ($active.length !== 0){
                        $active.show()
                    } else{
                        let correct = 0
                        for (index = 0; index < score.length; index++) {
                            if (score[index]){correct++}
                        }

                        let $summaryText = $("#summary-text")
                        $summaryText.html("You scored " + correct.toString() + "/" + score.length.toString() + ".")
                        if (correct/score.length > 0.7){
                            $summaryText.append(" Great work!")
                        }

                        $("#quiz-done").show()
                    }
                }, (2*messageSpeed)+messagePauseTime+100)
            }),
            error: (function () {
                let $body = $("body")
                $body.html("There was an error checking your response. Are you connected to wifi?")
                $body.append("<br><a href=''><button>Reload Quiz</button></a>")
            })
        })


    })

})
