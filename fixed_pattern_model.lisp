(defparameter *copying-area-y-shift* 500)

(clear-all)

(define-model drawing-test
    (sgp :trace-detail low)
    ; (sgp :trace-detail medium) ;; medium
    (sgp :v t  :unstuff-visual-location nil)
    (sgp :esc t :bll 0.5)
    (sgp :show-focus t :auto-attend t :needs-mouse t)
    (sgp :cursor-fitts-coeff 0.04)
    (sgp :visual-num-finsts 100 :visual-finst-span 300)
    (sgp :declarative-num-finsts 100 :declarative-finst-span 300 )
    (sgp :mas 22) ;; max associative strengh; S in equation Sij = S - ln(fan)
    ; (sgp :act t) ;; show activation trace
    ; (sgp :le 3)

    ; (set-parameter-value :show-focus 'blue)

    (chunk-type goal state task-type pattern-identified next-line-slot-name exploring-pattern tar-line-stim
                     retrieval-line-group-state chunking-root next-line-location
                     figure-right figure-left figure-top figure-bottom figure-centre cur-location-slot


                     next-line-retrieved pattern-retrieved figure-hierarchy-label figure-seen)
    (chunk-type (line-stimulus (:include visual-object)) color previous screen-x screen-y x-s y-s x-e y-e location type label)
    ; (chunk-type line-group type label x-s-1 y-s-1 x-e-1 y-e-1 x-s-2 y-s-2 x-e-2 y-e-2
    ;             x-s-3 y-s-3 x-e-3 y-e-3 x-s-4 y-s-4 x-e-4 y-e-4 line-label-1 line-label-2 line-label-3 line-label-4)
    (chunk-type (line-group (:include visual-object)) type label chunk-type-tag  screen-x screen-y
                                                        left right above below inside
                                                        line1 line2 line3 line4 line5 line6 line7 line8 line9 line10
                                                        line11 line12 line13 line14 line15 line16 line17 line18 line19 line20
                                                        line21 line22 line23 line24 line25 line26 line27 line28 line29 line30
                                                        location
    )
    (chunk-type figure label slot-1 slot-2 slot-3 slot-4 slot-5 slot-6 slot-7 slot-8 slot-9 slot-10
                             slot-11 slot-12 slot-13 slot-14 slot-15 slot-16 slot-17 slot-18 slot-19 slot-20
                             slot-21 slot-22 slot-23 slot-24 slot-25 slot-26 slot-27 slot-28 slot-29 slot-30
                            location
    )
    (define-chunks
        (trace) (copy) (delayedrecall) (immediaterecall)
        (found) (not-found)
        (figure-right) (figure-left) (figure-top) (figure-bottom) (figure-centre)

        (figure-right-chunk isa line-group)
        (figure-left-chunk isa line-group)
        (figure-top-chunk isa line-group)
        (figure-bottom-chunk isa line-group)
        (figure-centre-chunk isa line-group)

        (goal state start figure-right figure-right-chunk figure-left figure-left-chunk)
                          ; figure-top figure-top-chunk figure-bottom figure-bottom-chunk
                          ; figure-centre figure-centre-chunk)
    )
    (goal-focus goal )

    ; (set-visloc-default screen-x highest screen-y lowest)

    (P before-trial-start
        =goal>
            state               start
        ?visual-location>
            state               free
    ==>
        +visual-location>
            :attended            nil
            screen-y            lowest
            ; text                t
        =goal>
            state               finding-text-location
    )

    (P check-trial-task-type
        =goal>
            state               finding-text-location
        ?visual-location>
            state               free
            - buffer              failure
        ?visual>
            state               free
        =visual>
            text                t
            value               =task-type-str
    ==>
        !bind!                  =task-type (read-from-string =task-type-str)
        =goal>
            state               preparing-find-start-button-location
            task-type           =task-type
    )

    (P find-start-button-location
        =goal>
            state               preparing-find-start-button-location
        ?visual-location>
            state               free
    ==>
        +visual-location>
            :attended            nil
            screen-y            highest
            oval                t
        =goal>
            state               finding-start-button-location
    )

    (P move-cursor-to-start-button
        =goal>
            state               finding-start-button-location
        ?visual-location>
            state               free
        =visual-location>
        ?manual>
            state               free
    ==>
        +manual>
            cmd                 move-cursor
            loc                 =visual-location
        =goal>
            state               moving-cursor-to-start-button
    )

    (P press-start-button
        =goal>
            state               moving-cursor-to-start-button
        ?manual>
            state               free
    ==>
        +manual>
            cmd                 click-mouse
        =goal>
            state               pressing-start-button
    )

    ;;;;================================================================
    ;;;; Tracing trials
    ;;;;================================================================

    (P start-tracing-trial
        =goal>
            state               pressing-start-button
            task-type           trace
            ; task-type           copy
        ?manual>
            state               free
        ?visual>
            scene-change        t
    ==>
        !eval!                  ("create-line-chunks")
        =goal>
            state               preparing-retrieve-hash-location-trace
    )

    (P retrieve-hash-tag-chunk-trace
        =goal>
            state               preparing-retrieve-hash-location-trace
        ?retrieval>
            state               free
    ==>
        +retrieval>
            type                group-hash
        =goal>
            state               retrieving-hash-location-trace
    )

    (P find-figure-is-new
        =goal>
            state               retrieving-hash-location-trace
        ?retrieval>
            state               free
            buffer              failure
    ==>
        =goal>
            state               preparing-find-hash-from-top-left-trace
            retrieval-line-group-state  failure
    )

    (P find-figure-seen-before-trace
        =goal>
            state               retrieving-hash-location-trace
        ?retrieval>
            state               free
            - buffer            failure
        =retrieval>
            screen-x            =x
            screen-y            =y
        ?visual>
            state               free
        ?imaginal>
            state               free
    ==>
        !bind!                  =hash-location ("create-screen-location" =x =y)
        =retrieval>
        +visual>
            cmd                 move-attention
            screen-pos          =hash-location
        +imaginal>              =retrieval
        =goal>
            ; state               attending-to-hash-location-trace
            state               retrieving-hash-pattrern-trace
            retrieval-line-group-state  success
    )

    ; (P save-hash-pattern-into-imaginal-trace
    ; ==>
    ; )

    ; (P get-next-hash-line-base-on-dm-trace)

    (P find-hash-location-trace
        =goal>
            state               preparing-find-hash-from-top-left-trace
        ?visual-location>
            state               free
    ==>
        +visual-location>
            :attended            nil
            ; nearest             current
            ; screen-x            highest
            screen-y            lowest
            screen-x            highest
            color               "blue"
        =goal>
            state               attending-to-top-left-trace
    )

    ; (P move-attention-to-top-left-trace
    ;     =goal>
    ;         state               preparing-attend-to-top-left-trace
    ;     ?visual-location>
    ;         state               free
    ;     =visual-location>
    ;     ?visual>
    ;         state               free
    ; ==>
    ;     =visual-location>
    ;     +visual>
    ;         cmd                 move-attention
    ;         screen-pos          =visual-location
    ;     =goal>
    ;         state               attending-to-top-left-trace
    ; )

    ;; Put visibale lines into imaginal buffer, then test whether lines in
    ;; imaginal buffer comtains a hash tag pattern
    (P move-atttention-to-top-left-finish-trace
        =goal>
            state               attending-to-top-left-trace
        ?visual>
            state               free
        ?visual-location>
            state               free
            - buffer            failure
        =visual-location>
        ?imaginal>
            state               free
    ==>
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location)
        +imaginal>              =lines-chunk
        =goal>
            state               finding-hash-pattern-trace
    )

    (P find-hash-from-visible-line-trace
        =goal>
            state               finding-hash-pattern-trace
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =pattern-identified ("identify-pattern-from-recognisable-lines" =imaginal "hash")
        =goal>
            state               checking-hash-pattern-trace
            pattern-identified  =pattern-identified
    )

    (P find-hash-success-trace
        =goal>
            state               checking-hash-pattern-trace
            - pattern-identified  not-found
            pattern-identified  =pattern-identified
        ?visual>
            state               free
        ?imaginal>
            state               free
    ==>
        ; !bind!                  =pattern-chunk ("encode-pattern-by-label" "hash")
        ; +imaginal>                =pattern-chunk
        +imaginal>              =pattern-identified
        =goal>
            ; state               preparing-draw-hash-pattern-trace
            state               preparing-save-hash-pattern-trace
    )

    (P find-hash-failure-trace
        =goal>
            state               checking-hash-pattern-trace
            pattern-identified  not-found
        ?visual-location>
            state               free
    ==>
        +visual-location>
            :attended            nil
            ; :nearest            current-y
            :nearest            current
            color               "blue"
        =goal>
            state               finding-next-hash-line-locaiton-trace
    )


    (P attend-to-next-hash-line-finish-trace
        =goal>
            state               finding-next-hash-line-locaiton-trace
        ?imaginal>
            state               free
        =imaginal>
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
    ==>
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location =imaginal)
        +imaginal>              =lines-chunk
        =goal>
            state               finding-hash-pattern-trace
    )

    (P find-hash-tag-no-need-rehearsal-trace
        =goal>
            state               preparing-save-hash-pattern-trace
            retrieval-line-group-state  success
    ==>
        =goal>
            state               preparing-draw-hash-pattern-trace
    )

    (P memorise-hash-first-seen-trace
        =goal>
            state               preparing-save-hash-pattern-trace
            retrieval-line-group-state  failure
        ?imaginal>
            state               free
    ==>
        -imaginal>
        =goal>
            state               saving-hash-pattern-into-dm-trace
    )

    (P rehearse-hash-first-seen-trace
        =goal>
            state               saving-hash-pattern-into-dm-trace
        ?retrieval>
            state               free
    ==>
        +retrieval>
            isa                 line-group
            type                group-hash
        =goal>
            state               retrieving-hash-pattrern-trace
    )

    (P retrive-hash-pattern-success-trace
        =goal>
            state               retrieving-hash-pattrern-trace
        ?retrieval>
            state               free
        =retrieval>
        ?imaginal>
            state               free
    ==>
        +imaginal>              =retrieval
        =goal>
            state               preparing-draw-hash-pattern-trace
    )

    (P get-next-line-slot-of-hash-trace
        =goal>
            state               preparing-draw-hash-pattern-trace
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =next-slot ("get-next-line-group-chunk-slot" =imaginal)
        =goal>
            state               preparing-next-line-start-location-trace
            next-line-slot-name =next-slot
    )

    (P get-hash-line-from-DM-trace
        =goal>
            state               preparing-next-line-start-location-trace
            next-line-slot-name =next-slot
        ?imaginal>
            state               free
        =imaginal>
            =next-slot          =line-chunk
        ?retrieval>
            state               free
    ==>
        +retrieval>             =line-chunk
        =imaginal>
        =goal>
            state               retrieving-next-line-start-location-trace
    )

    (P find-hash-line-reproduced-finish-trace
        =goal>
            state               preparing-next-line-start-location-trace
            next-line-slot-name not-found
        ?visual-location>
            state               free
        ?imaginal>
            state               free
        =imaginal>
    ==>
        ; =imaginal>
        !eval!                  ("get-updated-root-chunk" =imaginal =goal)
        =goal>
            state               preparing-chunking-root-trace
    )

    (P put-chunking-root-into-imaginal-trace
        =goal>
            state               preparing-chunking-root-trace
            chunking-root       =chunking-root
        ?imaginal>
            state               free
    ==>
        +imaginal>              =chunking-root
        =goal>
            state               preparing-next-pattern-trace
    )

    (P retrieve-next-pattern-trace
        =goal>
            state               preparing-next-pattern-trace
            ; chunking-root       =chunking-root
        ?visual-location>
            state               free
        ?imaginal>
            state               free
        ?retrieval>
            state               free
    ==>
        +visual-location>
            :attended            nil
            :nearest            current
            color               "blue"
        +retrieval>
            ; location            =location-label
            chunk-type-tag      line-group
            :recently-retrieved nil
        =goal>
            state               attending-to-nearest-next-line-trace
            retrieval-line-group-state  retrieving
    )

    (P retrieve-chunk-success
        =goal>
            retrieval-line-group-state  retrieving
        ?retrieval>
            state               free
            - buffer             failure
            - buffer             empty
        ; ?visual>
        ;     state               busy
    ==>
        =goal>
            retrieval-line-group-state  retrieved
    )

    (P retrieve-chunk-failed
        =goal>
            retrieval-line-group-state  retrieving
        ?retrieval>
            state               free
            buffer              failure
    ==>
        =goal>
            retrieval-line-group-state  failure
    )

    (P get-start-location-of-hash-line-trace
        =goal>
            state               retrieving-next-line-start-location-trace
        ?retrieval>
            state               free
            - buffer            failure
        =retrieval>
            x-s                 =x
            y-s                 =y
        !bind!                  =line-start-location ("create-screen-location" =x =y)
        ?visual>
            state               free
        ?manual>
            state               free
    ==>
        !eval!                  ("record-response-type" =retrieval)
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-start-hash-line-trace
    )

    (P press-to-start-draw-hash-line-trace
        =goal>
            state               moving-attention-to-start-hash-line-trace
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            screen-x            =x
            screen-y            =y
        !bind!                  =line-screen-location ("create-screen-location" =x =y)
    ==>
        =retrieval>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =goal>
            state               pressed-for-start-hash-line-trace
    )

    (P move-hand-to-end-draw-hash-line-trace
        =goal>
            state               pressed-for-start-hash-line-trace
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            x-e                 =x
            y-e                 =y
        !bind!                  =line-end-location ("create-screen-location" =x =y)
    ==>
        !eval!                  ("record-response-time" "start")
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-hash-line-end-trace
    )

    (P draw-hash-line-finish-trace
        =goal>
            state               moving-hand-to-hash-line-end-trace
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =retrieval)
        =goal>
            state               preparing-draw-hash-pattern-trace
    )

    (P find-all-line-drawn-trace
        =goal>
            state               attending-to-nearest-next-line-trace
        ?visual>
            state               free
        ?visual-location>
            state               free
            buffer              failure
        !bind!                  =rtn ("check-all-line-are-drawn")
        !eval!                  (eq =rtn 'finish)
    ==>
        =goal>
            state               preparing-find-finish-button
    )

    (P find-remain-line-location-trace
        =goal>
            state               attending-to-nearest-next-line-trace
        ?visual>
            state               free
        ?visual-location>
            state               free
            buffer              failure
        ?retrieval>
            state               free
            buffer              failure
        ; ?manual>
        ;     state               free
        ; ?imaginal>
        ;     state               free
        ; !eval!                  (eq ("check-all-line-are-drawn") nil)
        !bind!                  =rtn ("check-all-line-are-drawn")
        !eval!                  (eq =rtn 'not-finish)
    ==>
        !bind!                  =tar-line ("get-location-of-unreproduced-line")
        !bind!                  =screen-x (chunk-slot-value-fct =tar-line 'screen-x)
        !bind!                  =screen-y (chunk-slot-value-fct =tar-line 'screen-y)
        ; !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =line-screen-location )
        ; !bind!                  =line-screen-location ("get-line-end-point-location" =tar-line "mid")
        ; +imaginal>              =lines-chunk
        ; +visual>
        ;     isa                 move-attention
        ;     screen-pos          =line-screen-location
        +visual-location>
            color               "blue"
            screen-x            =screen-x
            screen-y            =screen-y
        ; +manual>
        ;     isa                 move-cursor
        ;     loc                 =line-screen-location
        ; =visual-location>       =line-screen-location
        =goal>
            state               attending-to-nearest-next-line-trace
            ; state               preparing-find-pattern-from-nearby-line-trace
            tar-line-stim       =tar-line
    )

    ; (P atttend-on-remain-line-trace)

    (P find-finish-button
        =goal>
            state               preparing-find-finish-button
        ?visual-location>
            state               free
        ?retrieval>
            state               free
    ==>
        +retrieval>
            ; chunk-type-tag      line-group
            ; :recently-retrieved reset
        +visual-location>
            ; :attended           nil
            value               "Finish"
        =goal>
            state               finding-finish-button
    )

    (P find-finish-button-success
        =goal>
            state               finding-finish-button
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
        ?manual>
            state               free
    ==>
        +manual>
            cmd                 move-cursor
            loc                 =visual-location
        =goal>
            state               moving-cursor-to-finish-button
    )

    (P press-finish-button
        =goal>
            state               moving-cursor-to-finish-button
        ?manual>
            state               free
    ==>
        +manual>
            cmd                 click-mouse
        =goal>
            state               pressing-finish-button
    )

    (P start-next-trial
        =goal>
            state               pressing-finish-button
        ?manual>
            state               free
    ==>
        =goal>
            state               start
    )



    ;;; participants showed three possibilities:
    ;;; 1, start from box first
    ;;; 2, start from nose first
    ;;; 3, start from fin first
    ;;;
    ;;; The first pattern they choose is consitant for all four type of task
    (P find-nearest-line-success-trace
        =goal>
            state               attending-to-nearest-next-line-trace
            - retrieval-line-group-state  retrieved

        ?visual>
            state               free
        ?visual-location>
            state               free
            - buffer            failure
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
        ; ?retrieval>
        ;     state               free
    ==>
        ; !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location =imaginal)
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location )
        !bind!                  =tar-line ("get-fixated-line-chunk" =visual-location)
        =visual-location>
        !eval!                  ("clear-tmp-goal-chunk-imaginal" =imaginal)
        +imaginal>              =lines-chunk

        =goal>
            state               preparing-find-pattern-from-nearby-line-trace
            ; retrieval-line-group-state  retrieving
            tar-line-stim       =tar-line
            ; first-line-in-pattern  =visual-location
            ; cur-location-slot   =slot-name
    )




    (P recognise-pattern-from-nearby-lines-trace
        =goal>
            state               preparing-find-pattern-from-nearby-line-trace
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        =visual-location>
        !bind!                  =pattern-chunk ("identify-pattern-given-line-stim" =imaginal =visual-location)

        ; !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location)
        ; +imaginal>              =lines-chunk
        ; !bind!                  =slot-name ("get-goal-location-slot-name" =visual-location)
        ; !bind!                  =slot-val ("get-visible-symmetry-line" =visual-location =goal)
        =goal>
            state               finding-pattern-trace
            pattern-identified  =pattern-chunk
    )

    (P recognise-pattern-from-nearby-lines-failed-trace
        =goal>
            state               finding-pattern-trace
            pattern-identified  not-found
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
        ?visual>
            state               free
    ==>
        =imaginal>

        !bind!                  =next-tar-location ("get-furthest-pattern-line-location" =imaginal =visual-location)
        +visual>
            isa                 move-attention
            screen-pos          =next-tar-location
        =visual-location>       =next-tar-location
        =goal>
            state               moving-attention-to-next-pattern-line-trace
    )

    (P save-more-recognisable-into-imaginal-trace
        =goal>
            state               moving-attention-to-next-pattern-line-trace
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
    ==>
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location =imaginal)
        +imaginal>              =lines-chunk
        =visual-location>
        =goal>
            state               preparing-find-pattern-from-nearby-line-trace
    )

    (P recognise-pattern-from-nearby-lines-success-trace
        =goal>
            state               finding-pattern-trace
            - pattern-identified  not-found
            pattern-identified  =pattern-identified
        ?retrieval>
            state               free
    ==>
        ; !eval!                  (add-dm-chunks =pattern-identified)
        !bind!                  =pattern-label (chunk-slot-value-fct =pattern-identified 'label)
        +retrieval>
            chunk-type-tag      line-group
            label               =pattern-label
        =goal>
            state               preparing-draw-pattern-line-trace
    )


    ; (P find-pattern-reproduced-finish-trace
    ;     =goal>
    ;         state               test
    ;     ?retrieval>
    ;         state               free
    ;         buffer              failure
    ;     ?imaginal>
    ;         state               free
    ;     =imaginal>
    ; ==>
    ;     !eval!                  ("get-updated-root-chunk" =imaginal =goal)
    ;     =goal>
    ;         state               preparing-chunking-root-trace
    ;         ; state               end
    ; )

    (P move-hand-to-start-location-of-line-trace
        =goal>
            state               preparing-draw-pattern-line-trace
            tar-line-stim       =tar-line

        ; !bind!                  =line-start-location ("create-screen-location" (chunk-slot-value =tar-line x-s) (chunk-slot-value =tar-line x-y))
        !bind!                  =line-start-location ("get-line-end-point-location" =tar-line "start")
        ?visual>
            state               free
        ?manual>
            state               free
    ==>
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-line-start-location-trace
            ; state               end
    )

    (P press-to-start-draw-pattern-line-trace
        =goal>
            state               moving-attention-to-line-start-location-trace
            tar-line-stim       =tar-line
        ?manual>
            state               free
        ?visual>
            state               free
        !bind!                  =line-screen-location ("get-line-end-point-location" =tar-line "mid")
    ==>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =goal>
            state               pressed-for-start-pattern-line-trace
    )

    (P move-hand-to-end-draw-pattern-line-trace
        =goal>
            state               pressed-for-start-pattern-line-trace
            tar-line-stim       =tar-line
        ?manual>
            state               free
        ?visual>
            state               free
        !bind!                  =line-end-location ("get-line-end-point-location" =tar-line "end")
    ==>
        !eval!                  ("record-response-time" "start")
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-pattern-line-end-trace
    )

    (P draw-pattern-line-finish-trace
        =goal>
            state               moving-hand-to-pattern-line-end-trace
            tar-line-stim       =tar-line
        ?manual>
            state               free
        ?visual>
            state               free
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =tar-line)
        !eval!                  ("record-response-type" =tar-line)
        =goal>
            state               preparing-next-pattern-line-location-trace
    )

    (P get-next-pattern-line-location-trace
        =goal>
            state               preparing-next-pattern-line-location-trace
            tar-line-stim       =tar-line
        ?imaginal>
            state               free
            ; - buffer              empty
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =next-location ("get-next-pattern-line-location" =imaginal =tar-line)
        =goal>
            state               checking-next-pattern-line-location-trace
            next-line-location  =next-location
    )

    (P find-current-pattern-reproduce-finish-trace
        =goal>
            state               checking-next-pattern-line-location-trace
            next-line-location  not-found
            - pattern-identified  not-found
            pattern-identified  =pattern-identified
    ==>
        !eval!                  ("get-updated-root-chunk" =pattern-identified =goal)
        =goal>
            state               preparing-chunking-root-trace
    )

    (P move-attention-to-next-pattern-line-trace
        =goal>
            state               checking-next-pattern-line-location-trace
            - next-line-location  not-found
            next-line-location  =next-location
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
    ==>
        +visual>
            cmd                 move-attention
            screen-pos          =next-location
        =visual-location>       =next-location
        =goal>
            state               moving-attention-to-next-pattern-line-location-trace
    )

    (P attentd-to-next-pattern-line-finish-trace
        =goal>
            state               moving-attention-to-next-pattern-line-location-trace
        ?visual>
            state               free
        ?visual-location>
            state               free
        ?imaginal>
            state               free
        =imaginal>
        =visual-location>
    ==>
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location =imaginal)
        !bind!                  =tar-line ("get-fixated-line-chunk" =visual-location)
        =visual-location>
        +imaginal>              =lines-chunk
        =goal>
            state               preparing-find-pattern-from-nearby-line-trace
            tar-line-stim       =tar-line
    )

    ;;;; if a group chunk is retrieved, move attention to the group location
    (P find-line-group-is-retrieved-trace
        =goal>
            state               attending-to-nearest-next-line-trace
            retrieval-line-group-state  retrieved
        ; ?visual>
        ;     state               busy
        ; ?imaginal>
        ;     state               free
        ; =imaginal>
    ==>
        ; !eval!                  ("clear-tmp-goal-chunk-imaginal" =imaginal)
        =goal>
            state               preparing-attending-to-retrieved-pattern-trace
    )

    (P move-attention-to-retrieved-group-location-trace
        =goal>
            state               preparing-attending-to-retrieved-pattern-trace
        ?retrieval>
            state               free
        =retrieval>
            screen-x            =x
            screen-y            =y
        ?imaginal>
            state               free
        ; ?visual>
        ;     state               free
    ==>
        ; !bind!                  =group-location ("create-screen-location" =x =y)
        +imaginal>              =retrieval
        ; +visual>
        ;     isa                 move-attention
        ;     screen-pos          =group-location
        =goal>
            state               attending-to-retrieved-pattern-trace
    )

    (P get-pattern-line-from-DM-trace
        =goal>
            state               attending-to-retrieved-pattern-trace
        ?imaginal>
            state               free
        =imaginal>
            label               =pattern-label
        ?retrieval>
            state               free
    ==>
        +retrieval>
            label               =pattern-label
            :recently-retrieved nil
        =imaginal>
        =goal>
            state               retrieving-pattern-line-trace
    )

    (P find-pattern-reproduced-finish-by-dm-trace
        =goal>
            state               retrieving-pattern-line-trace
        ?retrieval>
            state               free
            buffer              failure
        ?imaginal>
            state               free
        =imaginal>
    ==>
        !eval!                  ("get-updated-root-chunk" =imaginal =goal)
        =goal>
            state               preparing-chunking-root-trace
    )

    ;;; move hand to start location of the line get from DM
    (P get-pattern-line-from-DM-success-trace
        =goal>
            state               retrieving-pattern-line-trace
        ?retrieval>
            state               free
            - buffer              failure
        =retrieval>
            x-s                 =x
            y-s                 =y
        !bind!                  =line-start-location ("create-screen-location" =x =y)
        ?visual>
            state               free
        ?manual>
            state               free
    ==>
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-line-start-location-dm-trace
    )

    (P press-to-start-draw-pattern-line-dm-trace
        =goal>
            state               moving-attention-to-line-start-location-dm-trace
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            screen-x            =x
            screen-y            =y
        !bind!                  =line-screen-location ("create-screen-location" =x =y)
    ==>
        =retrieval>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =goal>
            state               pressed-for-start-pattern-line-dm-trace
    )

    (P move-hand-to-end-draw-pattern-line-dm-trace
        =goal>
            state               pressed-for-start-pattern-line-dm-trace
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            x-e                 =x
            y-e                 =y
        !bind!                  =line-end-location ("create-screen-location" =x =y)
    ==>
        !eval!                  ("record-response-time" "start")
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-pattern-line-end-dm-trace
    )

    (P draw-pattern-line-finish-dm-trace
        =goal>
            state               moving-hand-to-pattern-line-end-dm-trace
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =retrieval)
        !eval!                  ("record-response-type" =retrieval)
        =goal>
            state               attending-to-retrieved-pattern-trace
    )



    ; (P find-hash-from-visible-line-failure-trace
    ;     =goal>
    ;         state               identifying-hash-trace
    ;     ?imaginal>
    ;         state               free
    ;     !eval!                  (not ("identify-pattern-from-imaginal" "hash"))
    ; ==>
    ;
    ;     =goal>
    ;         state               test-stop
    ; )


    ;;;;================================================================
    ;;;; Copying trials
    ;;;;================================================================

    (P start-copying-trial
        =goal>
            state               pressing-start-button
            task-type           copy
        ?manual>
            state               free
        ?visual>
            scene-change        t
    ==>
        ; !eval!                  ("create-line-chunks")
        =goal>
            state               preparing-retrieve-hash-location-copy
    )

    (P retrieve-hash-tag-chunk-copy
        =goal>
            state               preparing-retrieve-hash-location-copy
        ?retrieval>
            state               free
    ==>
        +retrieval>
            type                group-hash
        =goal>
            state               retrieving-hash-location-copy
    )

    (P find-hash-location-copy
        =goal>
            state               retrieving-hash-location-copy
        ?visual-location>
            state               free
    ==>
        +visual-location>
            :attended            nil
            ; nearest             current
            ; screen-x            highest
            screen-y            lowest
            screen-x            highest
            color               "blue"
        =goal>
            state               attending-to-top-left-copy
    )

    (P move-atttention-to-top-left-finish-copy
        =goal>
            state               attending-to-top-left-copy
        ?visual>
            state               free
        ?visual-location>
            state               free
            - buffer            failure
        =visual-location>
        ?imaginal>
            state               free
    ==>
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location)
        +imaginal>              =lines-chunk
        =goal>
            state               finding-hash-pattern-copy
    )

    (P find-hash-from-visible-line-copy
        =goal>
            state               finding-hash-pattern-copy
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =pattern-identified ("identify-pattern-from-recognisable-lines" =imaginal "hash")
        =goal>
            state               checking-hash-pattern-copy
            pattern-identified  =pattern-identified
    )

    (P find-hash-success-copy
        =goal>
            state               checking-hash-pattern-copy
            - pattern-identified  not-found
            pattern-identified  =pattern-identified
        ?visual>
            state               free
        ?imaginal>
            state               free
    ==>
        +imaginal>              =pattern-identified
        =goal>
            state               preparing-draw-hash-pattern-copy
    )

    (P find-hash-success-from-retrieval-copy
        =goal>
            state               checking-hash-pattern-copy
            pattern-identified  not-found
        ?visual-location>
            state               free
        ?retrieval>
            state               free
            - buffer              failure
        =retrieval>
        ?imaginal>
            state               free
    ==>
        +imaginal>              =retrieval
        =goal>
            state               preparing-draw-hash-pattern-copy
    )

    (P find-hash-failure-copy
        =goal>
            state               checking-hash-pattern-copy
            pattern-identified  not-found
        ?visual-location>
            state               free
        ?retrieval>
            state               free
            buffer              failure
    ==>
        +visual-location>
            :attended            nil
            :nearest            current
            color               "blue"
        =goal>
            state               finding-next-hash-line-locaiton-copy
    )

    (P attend-to-next-hash-line-finish-copy
        =goal>
            state               finding-next-hash-line-locaiton-copy
        ?imaginal>
            state               free
        =imaginal>
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
    ==>
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location =imaginal)
        +imaginal>              =lines-chunk
        =goal>
            state               finding-hash-pattern-copy
    )

    (P get-next-line-slot-of-hash-copy
        =goal>
            state               preparing-draw-hash-pattern-copy
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =next-slot ("get-next-line-group-chunk-slot" =imaginal)
        =goal>
            state               preparing-next-line-start-location-copy
            next-line-slot-name =next-slot
    )

    (P get-hash-line-from-DM-copy
        =goal>
            state               preparing-next-line-start-location-copy
            next-line-slot-name =next-slot
        ?imaginal>
            state               free
        =imaginal>
            =next-slot          =line-chunk
        ?retrieval>
            state               free
    ==>
        +retrieval>             =line-chunk
        =imaginal>
        =goal>
            state               retrieving-next-line-start-location-copy
    )

    (P find-hash-line-reproduced-finish-copy
        =goal>
            state               preparing-next-line-start-location-copy
            next-line-slot-name not-found
        ?visual-location>
            state               free
        ?imaginal>
            state               free
        =imaginal>
    ==>
        ; =imaginal>
        !eval!                  ("get-updated-root-chunk" =imaginal =goal)
        =goal>
            state               preparing-chunking-root-copy
    )

    (P get-start-location-of-hash-line-copy
        =goal>
            state               retrieving-next-line-start-location-copy
        ?retrieval>
            state               free
            - buffer            failure
        =retrieval>
            x-s                 =x
            y-s                 =y
        !bind!                  =line-start-location ("create-screen-location" =x =y)
        ?visual>
            state               free
        ?manual>
            state               free
    ==>
        !eval!                  ("record-response-type" =retrieval)
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-start-hash-line-copy
    )

    (P press-to-start-draw-hash-line-copy
        =goal>
            state               moving-attention-to-start-hash-line-copy
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            screen-x            =x
            screen-y            =y
        !bind!                  =line-screen-location ("create-screen-location" =x =y)
    ==>
        =retrieval>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =goal>
            state               pressed-for-start-hash-line-copy
    )

    (P move-hand-to-end-draw-hash-line-copy
        =goal>
            state               pressed-for-start-hash-line-copy
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            x-e                 =x
            y-e                 =y
        !bind!                  =line-end-location ("create-screen-location" =x =y)
    ==>
        !eval!                  ("record-response-time" "start")
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-hash-line-end-copy
    )

    (P draw-hash-line-finish-copy
        =goal>
            state               moving-hand-to-hash-line-end-copy
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =retrieval)
        =goal>
            state               preparing-draw-hash-pattern-copy
    )


    (P put-chunking-root-into-imaginal-copy
        =goal>
            state               preparing-chunking-root-copy
            chunking-root       =chunking-root
        ?imaginal>
            state               free
    ==>
        +imaginal>              =chunking-root
        =goal>
            state               preparing-next-pattern-copy
    )

    (P prepare-next-pattern-location-copy
        =goal>
            state               preparing-next-pattern-copy
            ; chunking-root       =chunking-root
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
    ==>
        !bind!                  =next-pattern-line ("get-next-pattern-line-name-copying" =visual-location)
        =goal>
            state               checking-response-finished-copy
            tar-line-stim       =next-pattern-line
    )

    (P find-all-line-drawn-copy
        =goal>
            state               checking-response-finished-copy
            tar-line-stim       not-found
        ?retrieval>
            state               free
        ?visual-location>
            state               free
        ?visual>
            state               free
    ==>
        =goal>
            state               preparing-find-finish-button
            ; state               end
    )

    (P attend-to-next-pattern-location-copy
        =goal>
            state               checking-response-finished-copy
            - tar-line-stim       not-found
            tar-line-stim       =next-pattern-line
        ?retrieval>
            state               free
        ?visual-location>
            state               free
    ==>
        !bind!                  =end-x ("get-line-end-coord-copying" =next-pattern-line "x")
        !bind!                  =end-y ("get-line-end-coord-copying" =next-pattern-line "y")
        +visual-location>
            color               "blue"
            end2-x               =end-x
            end2-y               =end-y
        +retrieval>
            chunk-type-tag      line-group
            :recently-retrieved nil

        =goal>
            state               attending-to-nearest-next-line-copy
            retrieval-line-group-state  retrieving
    )

    (P attend-to-next-pattern-location-success-copy
        =goal>
            state               attending-to-nearest-next-line-copy
            - retrieval-line-group-state  retrieved
        ?visual>
            state               free
        ?visual-location>
            state               free
            - buffer            failure
        =visual-location>
        ?imaginal>
            state               free
    ==>
        ; !eval!                  ("break-point")
        !bind!                  =stim-location ("update-visual-location-for-copying" =visual-location)
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =stim-location )
        !bind!                  =tar-line ("get-fixated-line-chunk" =stim-location)
        =visual-location>
        +imaginal>              =lines-chunk
        =goal>
            state               preparing-find-pattern-from-nearby-line-copy
            tar-line-stim       =tar-line
    )

    (P recognise-pattern-from-nearby-lines-copy
        =goal>
            state               preparing-find-pattern-from-nearby-line-copy
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        =visual-location>
        !bind!                  =stim-location ("update-visual-location-for-copying" =visual-location)
        !bind!                  =pattern-chunk ("identify-pattern-given-line-stim" =imaginal =stim-location)
        =goal>
            state               finding-pattern-copy
            pattern-identified  =pattern-chunk
    )

    (P recognise-pattern-from-nearby-lines-failed-copy
        =goal>
            state               finding-pattern-copy
            pattern-identified  not-found
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
        ?visual>
            state               free
    ==>
        =imaginal>
        !bind!                  =stim-location ("update-visual-location-for-copying" =visual-location)
        !bind!                  =next-pattern-line ("get-furthest-pattern-line-chunk" =imaginal =stim-location)
        !bind!                  =end-x ("get-line-end-coord-copying" =next-pattern-line "x")
        !bind!                  =end-y ("get-line-end-coord-copying" =next-pattern-line "y")
        +visual-location>
            color               "blue"
            end2-x               =end-x
            end2-y               =end-y
        =goal>
            state               moving-attention-to-next-pattern-line-copy
    )

    (P save-more-recognisable-into-imaginal-copy
        =goal>
            state               moving-attention-to-next-pattern-line-copy
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
        ?imaginal>
            state               free
        =imaginal>
    ==>
        !bind!                  =stim-location ("update-visual-location-for-copying" =visual-location)
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =stim-location =imaginal)
        +imaginal>              =lines-chunk
        =visual-location>
        =goal>
            state               preparing-find-pattern-from-nearby-line-copy
    )

    (P recognise-pattern-from-nearby-lines-success-copy
        =goal>
            state               finding-pattern-copy
            - pattern-identified  not-found
            pattern-identified  =pattern-identified
        ?retrieval>
            state               free
        ?imaginal>
            state               free
    ==>
        !bind!                  =pattern-label (chunk-slot-value-fct =pattern-identified 'label)
        !eval!                  (merge-dm-fct (list (chunk-spec-to-chunk-def (chunk-name-to-chunk-spec =pattern-identified))))
        +retrieval>
            chunk-type-tag      line-group
            label               =pattern-label
        +imaginal>              =pattern-identified
        =goal>
            state               preparing-draw-pattern-line-copy
    )

    (P move-attention-to-pattern-location-copy
        =goal>
            state               preparing-draw-pattern-line-copy
            pattern-identified  =pattern-identified
        ?retrieval>
            state               free
        ?imaginal>
            state               free
        ?visual>
            state               free
    ==>
        !bind!                  =x (chunk-slot-value-fct =pattern-identified 'screen-x)
        !bind!                  =y (chunk-slot-value-fct =pattern-identified 'screen-y)
        !bind!                  =pattern-label (chunk-slot-value-fct =pattern-identified 'label)
        !bind!                  =pattern-location ("create-screen-location" =x =y)
        +visual>
            isa                 move-attention
            screen-pos          =pattern-location
        +retrieval>
            - chunk-type-tag      line-group
            label               =pattern-label
            :recently-retrieved nil
        =goal>
            state               retrieving-pattern-line-copy
    )

    (P move-hand-to-start-location-of-line-copy
        =goal>
            state               retrieving-pattern-line-copy
            ; tar-line-stim       =tar-line

        ?visual>
            state               free
        ?manual>
            state               free
        ?retrieval>
            state               free
            - buffer              failure
        =retrieval>
    ==>
        =retrieval>
        !bind!                  =line-start-location ("get-line-end-point-location" =retrieval "start")
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-line-start-location-copy
    )

    ; (P move-hand-to-start-location-of-line-copy
    ;     =goal>
    ;         state               preparing-draw-pattern-line-copy
    ;         tar-line-stim       =tar-line
    ;     !bind!                  =line-start-location ("get-line-end-point-location" =tar-line "start")
    ;     ?visual>
    ;         state               free
    ;     ?manual>
    ;         state               free
    ; ==>
    ;     +visual>
    ;         isa                 move-attention
    ;         screen-pos          =line-start-location
    ;     +manual>
    ;         isa                 move-cursor
    ;         loc                 =line-start-location
    ;     =goal>
    ;         state               moving-attention-to-line-start-location-copy
    ; )

    (P press-to-start-draw-pattern-line-copy
        =goal>
            state               moving-attention-to-line-start-location-copy
            ; tar-line-stim       =tar-line
        ?manual>
            state               free
        ?visual>
            state               free
        ?visual-location>
            state               free
        =visual-location>
        ?retrieval>
            state               free
        =retrieval>
        !bind!                  =line-screen-location ("get-line-end-point-location" =retrieval "mid")
    ==>
        =retrieval>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =visual-location>       =line-screen-location
        =goal>
            state               pressed-for-start-pattern-line-copy
    )

    (P move-hand-to-end-draw-pattern-line-copy
        =goal>
            state               pressed-for-start-pattern-line-copy
            ; tar-line-stim       =tar-line
        ?manual>
            state               free
        ?visual>
            state               free
        ?retrieval>
            state               free
        =retrieval>
        !bind!                  =line-end-location ("get-line-end-point-location" =retrieval "end")
    ==>
        =retrieval>
        !eval!                  ("record-response-time" "start")
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-pattern-line-end-copy
    )

    (P draw-pattern-line-finish-copy
        =goal>
            state               moving-hand-to-pattern-line-end-copy
            ; tar-line-stim       =tar-line
        ?manual>
            state               free
        ?visual>
            state               free
        ?retrieval>
            state               free
        =retrieval>
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =retrieval)
        !eval!                  ("record-response-type" =retrieval)
        =goal>
            state               preparing-next-pattern-line-location-copy
    )

    (P get-next-pattern-line-from-dm-copy
        =goal>
            state               preparing-next-pattern-line-location-copy
        ?imaginal>
            state               free
        =imaginal>
        ?retrieval>
            state               free
    ==>
        =imaginal>
        !bind!                  =pattern-label (chunk-slot-value-fct =imaginal 'label)
        +retrieval>
            - chunk-type-tag      line-group
            label               =pattern-label
            :recently-retrieved nil
        =goal>
            state               retrieving-pattern-line-copy
    )

    (P check-pattern-reproduce-finish-copy
        =goal>
            state               retrieving-pattern-line-copy
        ?retrieval>
            state               free
            buffer              failure
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =next-line ("check_whether_pattern_is_copy_finished" =imaginal)
        =goal>
            state               checking-pattern-finished-copy
            tar-line-stim       =next-line
    )

    (P find-pattern-not-reproduce-finish-copy
        =goal>
            state               checking-pattern-finished-copy
            - tar-line-stim       not-found
            tar-line-stim       =next-line
        ?visual-location>
            state               free
        ?visual>
            state               free
    ==>
        !bind!                  =end-x ("get-line-end-coord-copying" =next-line "x")
        !bind!                  =end-y ("get-line-end-coord-copying" =next-line "y")
        +visual-location>
            color               "blue"
            end2-x               =end-x
            end2-y               =end-y
        =goal>
            state               attending-to-rest-pattern-line-copy
    )

    (P memorize-rest-pattern-line-copy
        =goal>
            state               attending-to-rest-pattern-line-copy
            tar-line-stim       =next-line
        ?visual-location>
            state               free
            - buffer              failure
        ?retrieval>
            state               free
    ==>
        !eval!                  (merge-dm-fct (list (chunk-spec-to-chunk-def (chunk-name-to-chunk-spec =next-line))))
        +retrieval>             =next-line
        =goal>
            state               retrieving-pattern-line-copy
    )

    (P find-pattern-reproduce-finished-copy
        =goal>
            state               checking-pattern-finished-copy
            tar-line-stim       not-found
    ==>
        =goal>
            state               preparing-chunking-root-copy
    )

    ; (P get-next-pattern-line-location-copy
    ;     =goal>
    ;         state               preparing-next-pattern-line-location-copy
    ;         tar-line-stim       =tar-line
    ;     ?imaginal>
    ;         state               free
    ;     =imaginal>
    ; ==>
    ;     =imaginal>
    ;     !bind!                  =next-location ("get-next-pattern-line-location" =imaginal =tar-line)
    ;     =goal>
    ;         state               checking-next-pattern-line-location-copy
    ;         next-line-location  =next-location
    ; )

    ; (P move-attention-to-next-pattern-line-copy
    ;     =goal>
    ;         state               checking-next-pattern-line-location-copy
    ;         - next-line-location  not-found
    ;         next-line-location  =next-location
    ;     ?visual>
    ;         state               free
    ;     ?visual-location>
    ;         state               free
    ;     =visual-location>
    ; ==>
    ;     +visual>
    ;         cmd                 move-attention
    ;         screen-pos          =next-location
    ;     =visual-location>       =next-location
    ;     =goal>
    ;         state               moving-attention-to-next-pattern-line-location-copy
    ; )
    ;
    ; (P attentd-to-next-pattern-line-finish-copy
    ;     =goal>
    ;         state               moving-attention-to-next-pattern-line-location-copy
    ;     ?visual>
    ;         state               free
    ;     ?visual-location>
    ;         state               free
    ;     ?imaginal>
    ;         state               free
    ;     =imaginal>
    ;     =visual-location>
    ; ==>
    ;     !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =visual-location =imaginal)
    ;     !bind!                  =tar-line ("get-fixated-line-chunk" =visual-location)
    ;     =visual-location>
    ;     +imaginal>              =lines-chunk
    ;     =goal>
    ;         state               preparing-find-pattern-from-nearby-line-copy
    ;         tar-line-stim       =tar-line
    ; )

    (P find-current-pattern-reproduce-finish-copy
        =goal>
            state               checking-next-pattern-line-location-copy
            next-line-location  not-found
            - pattern-identified  not-found
            pattern-identified  =pattern-identified
    ==>
        !eval!                  ("get-updated-root-chunk" =pattern-identified =goal)
        =goal>
            state               preparing-chunking-root-copy
    )

    (P find-pattern-is-retrieved-during-attending-copy
        =goal>
            state               attending-to-nearest-next-line-copy
            retrieval-line-group-state  retrieved
        ?retrieval>
            state               free
        =retrieval>
        ?imaginal>
            state               free
    ==>
        !eval!                  ("break-point")
        !bind!                  =next-line ("check_whether_pattern_is_copy_finished" =retrieval)
        +imaginal>              =retrieval
        =goal>
            state               preparing-attending-to-retrieved-pattern-copy
            tar-line-stim       =next-line
    )

    (P find-retrieved-pattern-is-reproduced-copy
        =goal>
            state               preparing-attending-to-retrieved-pattern-copy
            tar-line-stim       not-found
    ==>
        =goal>
            state               attending-to-nearest-next-line-copy
            retrieval-line-group-state  failure
    )

    (P attend-to-retrieved-pattern-location-copy
        =goal>
            state               preparing-attending-to-retrieved-pattern-copy
            - tar-line-stim       not-found
            tar-line-stim       =next-line
        ?visual-location>
            state               free
        ?visual>
            state               free
    ==>
        !bind!                  =end-x ("get-line-end-coord-copying" =next-line "x")
        !bind!                  =end-y ("get-line-end-coord-copying" =next-line "y")
        +visual-location>
            color               "blue"
            end2-x               =end-x
            end2-y               =end-y
        =goal>
            state               attending-to-retrieved-pattern-copy
    )

    (P attend-to-etrieved-pattern-location-success-copy
        =goal>
            state               attending-to-retrieved-pattern-copy
        ?visual>
            state               free
        ?visual-location>
            state               free
            - buffer            failure
        =visual-location>
        ?imaginal>
            state               free
    ==>
        !eval!                  ("break-point")
        !bind!                  =stim-location ("update-visual-location-for-copying" =visual-location)
        !bind!                  =lines-chunk ("get-recognisable-lines-chunk" =stim-location )
        ; !bind!                  =tar-line ("get-fixated-line-chunk" =stim-location)
        =visual-location>
        +imaginal>              =lines-chunk
        =goal>
            state               preparing-find-pattern-from-nearby-line-copy
            ; tar-line-stim       =tar-line
    )



    ;;;;================================================================
    ;;;; Recalling trials
    ;;;;================================================================

    (P start-delayed-rcall-trial
        =goal>
            state               pressing-start-button
            task-type           delayedrecall
        ?manual>
            state               free
        ?visual>
            scene-change        t
    ==>
        =goal>
            state               preparing-retrieve-hash-location-recall
    )

    (P start-immediate-rcall-trial
        =goal>
            state               pressing-start-button
            task-type           immediaterecall
        ?manual>
            state               free
        ?visual>
            scene-change        t
    ==>
        =goal>
            state               preparing-retrieve-hash-location-recall
    )

    (P retrieve-hash-tag-chunk-recall
        =goal>
            state               preparing-retrieve-hash-location-recall
        ?retrieval>
            state               free
    ==>
        +retrieval>
            type                group-hash
        =goal>
            state               retrieving-hash-location-recall
    )

    (P retrieve-hash-success-recall
        =goal>
            state               retrieving-hash-location-recall
        ?retrieval>
            state               free
            - buffer              failure
        =retrieval>
        ?imaginal>
            state               free
    ==>
        +imaginal>              =retrieval
        =goal>
            state               preparing-draw-hash-pattern-recall
    )

    (P retrieve-hash-failure-recall
        =goal>
            state               checking-hash-pattern-recall
        ?retrieval>
            state               free
            buffer              failure
    ==>
        =goal>
            state               end
    )

    (P get-next-line-slot-of-hash-recall
        =goal>
            state               preparing-draw-hash-pattern-recall
        ?imaginal>
            state               free
        =imaginal>
    ==>
        =imaginal>
        !bind!                  =next-slot ("get-next-line-group-chunk-slot" =imaginal)
        =goal>
            state               preparing-next-line-start-location-recall
            next-line-slot-name =next-slot
    )

    (P get-hash-line-from-DM-recall
        =goal>
            state               preparing-next-line-start-location-recall
            next-line-slot-name =next-slot
        ?imaginal>
            state               free
        =imaginal>
            =next-slot          =line-chunk
        ?retrieval>
            state               free
    ==>
        +retrieval>             =line-chunk
        =imaginal>
        =goal>
            state               retrieving-next-line-start-location-recall
    )

    (P find-hash-line-reproduced-finish-recall
        =goal>
            state               preparing-next-line-start-location-recall
            next-line-slot-name not-found
    ==>
        =goal>
            state               preparing-chunking-root-recall
    )

    (P get-start-location-of-hash-line-recall
        =goal>
            state               retrieving-next-line-start-location-recall
        ?retrieval>
            state               free
            - buffer            failure
        =retrieval>
            x-s                 =x
            y-s                 =y
        !bind!                  =line-start-location ("create-screen-location" =x =y)
        ?visual>
            state               free
        ?manual>
            state               free
    ==>
        !eval!                  ("record-response-type" =retrieval)
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-start-hash-line-recall
    )

    (P press-to-start-draw-hash-line-recall
        =goal>
            state               moving-attention-to-start-hash-line-recall
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            screen-x            =x
            screen-y            =y
        !bind!                  =line-screen-location ("create-screen-location" =x =y)
    ==>
        =retrieval>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =goal>
            state               pressed-for-start-hash-line-recall
    )

    (P move-hand-to-end-draw-hash-line-recall
        =goal>
            state               pressed-for-start-hash-line-recall
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            x-e                 =x
            y-e                 =y
        !bind!                  =line-end-location ("create-screen-location" =x =y)
    ==>
        !eval!                  ("record-response-time" "start")
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-hash-line-end-recall
    )

    (P draw-hash-line-finish-recall
        =goal>
            state               moving-hand-to-hash-line-end-recall
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =retrieval)
        =goal>
            state               preparing-draw-hash-pattern-recall
    )

    (P put-chunking-root-into-imaginal-recall
        =goal>
            state               preparing-chunking-root-recall
            chunking-root       =chunking-root
        ?imaginal>
            state               free
    ==>
        +imaginal>              =chunking-root
        =goal>
            state               preparing-next-pattern-recall
    )

    (P retrieve-next-pattern-recall
        =goal>
            state               preparing-next-pattern-recall
        ?retrieval>
            state               free
    ==>
        +retrieval>
            chunk-type-tag      line-group
            :recently-retrieved nil
        =goal>
            state               retrieving-next-pattern-recall
    )

    (P retrieve-next-pattern-success-recall
        =goal>
            state               retrieving-next-pattern-recall
        ?imaginal>
            state               free
        ?retrieval>
            state               free
        =retrieval>
    ==>
        +imaginal>              =retrieval
        =goal>
            state               preparing-pattern-line-recall
    )

    (P retrieve-next-pattern-failed-recall
        =goal>
            state               retrieving-next-pattern-recall
        ?retrieval>
            state               free
            buffer              failure
    ==>
        =goal>
            state               preparing-find-finish-button
    )

    (P retrieve-pattern-line-recall
        =goal>
            state               preparing-pattern-line-recall
        ?retrieval>
            state               free
        ?imaginal>
            state               free
        =imaginal>
            label               =pattern-label
    ==>
        =imaginal>
        +retrieval>
            - chunk-type-tag      line-group
            label               =pattern-label
            :recently-retrieved nil
        =goal>
            state               retrieving-pattern-line-recall
    )

    (P retrieve-pattern-line-failed-recall
        =goal>
            state               retrieving-pattern-line-recall
        ?retrieval>
            state               free
            buffer              failure
    ==>
        =goal>
            state               preparing-next-pattern-recall
    )

    (P retrieve-pattern-line-success-recall
        =goal>
            state               retrieving-pattern-line-recall
        ?retrieval>
            state               free
            - buffer              failure
        =retrieval>
            x-s                 =x
            y-s                 =y
        !bind!                  =line-start-location ("create-screen-location" =x =y)
        ?visual>
            state               free
        ?manual>
            state               free
    ==>
        !eval!                  ("record-response-type" =retrieval)
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-start-location
        +manual>
            isa                 move-cursor
            loc                 =line-start-location
        =goal>
            state               moving-attention-to-start-pattern-line-recall
    )

    (P press-to-start-draw-pattern-line-recall
        =goal>
            state               moving-attention-to-start-pattern-line-recall
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            screen-x            =x
            screen-y            =y
        !bind!                  =line-screen-location ("create-screen-location" =x =y)
    ==>
        =retrieval>
        +manual>
            cmd                 punch
            hand                right
            finger              index
        +visual>
            isa                 move-attention
            screen-pos          =line-screen-location
        =goal>
            state               pressed-for-start-pattern-line-recall
    )

    (P move-hand-to-end-draw-pattern-line-recall
        =goal>
            state               pressed-for-start-pattern-line-recall
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
            x-e                 =x
            y-e                 =y
        !bind!                  =line-end-location ("create-screen-location" =x =y)
    ==>
        !eval!                  ("record-response-time" "start")
        =retrieval>
        +visual>
            isa                 move-attention
            screen-pos          =line-end-location
        +manual>
            isa                 move-cursor
            loc                 =line-end-location
        =goal>
            state               moving-hand-to-pattern-line-end-recall
    )

    (P draw-pattern-line-finish-recall
        =goal>
            state               moving-hand-to-pattern-line-end-recall
        ?manual>
            state               free
        ?visual>
            state               free
        =retrieval>
    ==>
        !eval!                  ("record-response-time" "end")
        !eval!                  ("add-responded-line" =retrieval)
        =goal>
            state               preparing-pattern-line-recall
    )

)
