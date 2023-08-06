/*
# Yet Another TermCast Viewer

The thingy can play .json files as produced from TermCast

The recordings can be flows with timings or shots, without timings - TermCast offers a switch for that (-S)

## Usage
    <termcast
          src="/assets/my_recording.json"
          [outer_scrolls="xy"]
          [inner_scrolls="y"]
          [inner_bgcol="black"]
          [rows="10"]
      />

    <termcast src="/assets/my_recording.json" />


## Requirements

- RxJS 5(!, sorry), xterm2.js
- Casts in json, like [[<contframe1>, ts1], ...]
- They SHOULD contain a first item indicating meta data, mainly rows cols of recording
- They should not have been resized during recording


## Dev

'Redux' single state architecture combined with RX / cycle.js:
All state kept in 'tag.s.state' (like a redux store)
- pushed through one stream (RX)
- catching ALL user intent (cycle)
- realizing the intent in a stream subscription only, updating screen and state

=> Forbidden to change the state (tag) within the stream, only allowed before
the stream starts (setup) and in its subscription.  In the stream ops
themselves we just contemplate on the user intent and the necesssary screen
updates do to be done in the next cycle.

*/
function define_termcasts(window, document) {
    let dflt_rows=24, dflt_cols=80
    const dbg_stream = false; // show the main stream items
    const dbg_store = false; // show the store for any stream new item
    const stream = Rx.Observable; // matter of personal taste
    const empty$ = stream.empty();
    const tick_duration = 30; // every 30 ms a terminal update with new frames while playing

    let log = (x, ...args) => {
        console.log(x, ...args)
        return x
    };

    // functions
    let er = (el) => (el ? el : document);
    let forall = (l, f) => stream.from(l).subscribe(f)
    let by_tag_name = (name, el) => er(el).getElementsByTagName(name);
    let by_id = (id, el) => er(el).getElementById(id);
    let by_cls_name = (cls, el) => er(el).getElementsByClassName(cls);
    let get_elmt = (cls, el) => by_cls_name(cls, el)[0];
    let all_xterms = () => by_tag_name("xterm");
    let all_xterm_fetchs = () => by_tag_name("xterm_fetch");
    let all_casts = () => by_tag_name("termcast");
    let height = (el) => parseInt(window.getComputedStyle(el).height);
    let width = (el) => parseInt(window.getComputedStyle(el).width);
    // all clicks on an element
    let clicks$ = (name, el) => stream.fromEvent(by_cls_name(name, el), "click");
    let attr = (name, el, dflt) => {
        x = er(el).getAttribute(name);
        return x ? x : dflt;
    };

    String.prototype.replace_all = function (search, replacement) {
        var target = this;
        try {
            return target.replace(new RegExp(search, "g"), replacement);
        } catch (err) {
            return target;
        }
    };
    contained = (item, arr) => arr.indexOf(item) > -1;

    const { fromEvent } = Rx.Observable;
    function drag_and_drop(element) {
        /* only exception to the one stream concept.
         * D&D is a standard stream, will put into a lib.
         * Downside: Does not see escape keys
         * */
        const el = element;
        el.is_draggable = true;

        const mousemove = fromEvent(document, "mousemove");

        fromEvent(el, "mousedown")
            .flatMap((md) => {
                let d = md.target;
                while (!d.is_draggable) d = d.parentElement;
                // add window offset only if position of d is relative:
                const style = window.getComputedStyle;
                const startX = md.clientX, // + window.scrollX,
                    startY = md.clientY, // + window.scrollY,
                    startLeft = parseInt(style(d).left) || 0;
                startTop = parseInt(style(d).top) || 0;
                return mousemove
                    .map((mm) => {
                        mm.preventDefault();
                        return {
                            left: startLeft + mm.clientX - startX,
                            top: startTop + mm.clientY - startY,
                        };
                    })
                    .takeUntil(fromEvent(document, "mouseup"));
            })
            .subscribe((pos) => {
                el.style.top = pos.top + "px";
                el.style.left = pos.left + "px";
            });
    }

    function tag_html(mode, tag) {
        let help_table = get_help_table();
        switch (mode) {
            case "loading":
                let src = attr("src", tag);
                return `
                    <div><i class="fa fa-cloud-download" />
                        ...loading cast ${src}
                    </div>
                   `;
            case "loaded":
                // reformat, keep closing </i>: xmllint --format r | xmllint --c14n - clip
                return `
<div class="tc">
  <div class="termcast_player" style="color: #999" width="100%"v>
    <div class="term_controls">
      <i class="term_info fa fa-info-circle" title="info"></i>
      <i class="term_play_btn fa fa-play" title="play/resume"></i>
      <i class="term_loop fa fa-circle-notch" title="loop"></i>
      <i class="term_rewind fa fa-fast-backward" title="rewind"></i>
      <span class="right_float" style="position: relative; float: right; font-family: monospace"></span>
      <i class="fa fa-tachometer-alt" title="playback speed multiplier"></i>
      <span class="term_play_speed">1</span>
      <span class="term_timer"></span>
      <i class="term_maxmin fa fa-expand" title="toggle height"></i>
    </div>
  </div>
  <div class="term_wrap" style="position:relative; width: 100%; overflow: hidden ">
    <terminal />
    <div class="term_help_insert draggable" style="z-index: 2; cursor: pointer; position: absolute; visibility: hidden; top: 3px; left: 10px;">
            ${help_table}
        </div>
    <div class="search_words_insert draggable" style="z-index: 3; left: 50%; top: 20%; cursor: pointer; position: absolute; visibility: hidden;">
      <table>
        <tr>
          <td>Search Items<br></br><b>j</b>: Jump to next match,
                <b>\n</b>: search linebreaks. Tip: use prompt to jump through cmds</td>
        </tr>
        <tr>
          <td>
            <input class="search_words has_user_input" width="100%"></input>
          </td>
        </tr>
      </table>
    </div>
    <!--i class="term_play_btn_big fa fa-5x fa-play" style="color: #777; z-index: 1; position: absolute;"></i-->
  </div>
  <div class="controls hidden">
      <a class="toggle-play-list" href="#">
        <i class="fa fa-list-ul"></i>
      </a>
      <div class="progress"> <div class="bar"></div> </div>
      <div class="duration clearfix">
        <span class="pull-left play-position"></span>
        <span class="pull-right"><span class="play-current-time">00:00:00</span> / <span class="play-total-time">00:00:00</span><span>&nbsp;</span>
            </span>
      </div>
      <div class="action-button">
        &nbsp;
        <a class="prev" href="#">       <i class="fa fa-step-backward" /></i> </a>
        <a class="play-pause" href="#"> <i class="fa fa-play"></i> </a>
        <a class="next" href="#">       <i class="fa fa-step-forward"></i> </a>

        <input class="volume" data-css="0.5" max="1" min="0" step="0.1" type="range" value="0.5"></input>
    </div>
  </div>
</div>
    `;
        }
    }

    function dbg(e) {
        debugger;
        return e;
        //console.log(els.selectionStart)
    }

    /* ------------------------------------------------------------------------- *
     *                      HANDLING USER INTENT (subscr to main stream)
     * ------------------------------------------------------------------------- */
    function reset(tag) {
        tag.s.cur_time = 0;
        tag.s.next_frame_nr = 0;
        tag.s.cast_ended = false;
        tag.s.is_playing = false;
    }

    do_search_terms = (tag, r) => {
        let hilite = r.ev.user_input;
        reset(tag);
        try {
            log("regexing", hilite);
            tag.s.hilite = tag.s.jump_str = new RegExp(hilite);
        } catch (err) {
            log(err.message);
            tag.s.hilite = "";
        }
    }

    do_update_controls_view = (tag) => {
        return
        /* done instantly at any change, i.e. also within stream */
        // first reset all:
        let speed = get_elmt("term_play_speed", tag);
        speed.innerHTML = "" + 2 ** tag.s.play_speed;
        let bb = get_elmt("term_play_btn_big", tag);
        bb.style.visibility = "hidden";
        let clloop = get_elmt("term_loop", tag).classList;

        clloop.remove("fa-spin");
        let cl = get_elmt("term_play_btn", tag).classList;
        stream
            .from(["fa-pause", "fa-play", "fa-stop-circle-o", "fa-step-forward"])
            .subscribe((x) => cl.remove(x));

        if (tag.s.is_shot) {
            get_elmt("termcast_player", tag).style.visibility = "hidden";
        }

        if (tag.s.cast_ended) cl.add("fa-stop-circle-o");
        else if (tag.s.is_playing) cl.add("fa-pause");
        else if (tag.s.do_one) cl.add("fa-step-forward");
        else if (tag.s.do_one_back) cl.add("fa-step-backward");
        else {
            cl.add("fa-play");
            bb.style.visibility = "visible";
        }

        tag.s.is_playing && tag.s.looping ? clloop.add("fa-spin") : 0;
        return tag;
    }



    function show_hide(tag, cls) {
        let el = get_elmt(cls, tag);
        let before = el.style.visibility;
        el.style.visibility = before == "hidden" ? "visible" : "hidden";
        if (before == "visible") tag.term.focus();
        // focus on first element with user input - if any:
        else
            stream
                .from([get_elmt("has_user_input", el)])
                .take(1)
                .filter((it) => it)
                .subscribe((it) => it.focus());
        return before == "hidden";
    }

    do_quit_play = (tag)     => tag.s.is_playing = false
    do_scroll_top = (tag)    => tag.term.scrollToTop();
    do_toggle_info = (tag)   => show_hide(tag, "term_help_insert");
    do_toggle_search = (tag) => show_hide(tag, "search_words_insert");
    do_escape = (tag) => {
        stream
            .from(by_cls_name("draggable", tag))
            .subscribe((el) => (el.style.visibility = "hidden"));
        tag.term.textarea.focus();
    }
    do_toggle_maxmin = (tag) => {
        tag.s.fullscreen = !tag.s.fullscreen;
        let tw = get_elmt("term_wrap", tag);
        let cl = get_elmt("term_maxmin", tag).classList;
        let trr = tag.s.recorder_rows;
        cl.remove("fa-expand");
        cl.remove("fa-compress");

        if (tag.s.fullscreen) {
            cl.add("fa-compress");
            tag.s.old_geo = tag.term.geometry;
            if (trr && trr != tag.s.old_geo[1]) {
                tag.term.resize(tag.s.recorder_cols, trr);
            } else {
                // use what we have
                let H = height(by_tag_name("body")[0]);
                let W = width(by_tag_name("body")[0]);
                let cm = tag.term.charMeasure;
                tag.term.resize(parseInt(W / cm.width), parseInt(H / cm.height));
            }
            if (!tag.s.is_playing) tag.s.is_playing = true;
        } else {
            cl.add("fa-expand");
            tag.term.resize(tag.s.old_geo[0], tag.s.old_geo[1]);
        }
    }

    do_toggle_speed = (tag, r) => {
        let cs = tag.s.play_speed;
        tag.s.play_speed = r.ev.key == "s" ? cs - 1 : r.ev.key == "d" ? 0 : cs + 1;
    }

    do_toggle_loop = (tag) => {
        /* the loop button also starts but does not stop the cast */
        // if playing, keep playing, else start
        tag.s.looping = !tag.s.looping; // || ! tag.s.is_playing
        if (!tag.s.is_playing) do_toggle_play(tag);
    }

    do_toggle_play = (tag) => {
        tag.s.is_playing = !tag.s.is_playing;
        if (tag.s.cast_ended) {
            reset(tag);
            tag.s.is_playing = true;
        }
        ctrl_update(tag)
    }


    do_toggle_rewind = (tag) => {
        reset(tag);
        tag.s.is_playing = true;
    }

    do_one = (tag, r) => {
        // realized in push_framesets
        tag.s.do_one = 1;
        tag.s.is_playing = false;
    }

    do_one_back = (tag, r) => {
        tag.s.jump_frame = Math.max(tag.s.next_frame_nr - 1, 0);
        reset(tag);
    }

    const do_jump = (tag, r) => {
        tag.s.jump_str = tag.s.last_jump;
    }



    do_scroll_bottom = (tag) => {
        tag.term.scrollToBottom();
    }

    function dispatch_intent_function(r) {
        // r.side_effect e.g. "do_scroll_top" - we call the do_scoll_up function here
        if (!r.side_effect) return;
        debugger;
        TC[r.side_effect](r.tag, r);
    }

    function add_intent_function(r) {
        if (r.frames) return r;
        if (r.ev.key != "c") r.ev.preventDefault();
        let func, funcs, inp;
        if (contained(r.ev.type, ["keyup", "keypress"])) {
            r["ev_type"] = "key";
            inp = r.ev.user_input;
            if (inp && inp.length > 0) func = "do_search_terms";
            else if (r.ev.key == "Escape") func = "do_escape";
            else {
                log("intent key: " + r.ev.key);
                stream
                    .from([
                        ["sdf", "do_toggle_speed"],
                        [" ", "do_toggle_play"],
                        ["q", "do_quit_play"],
                        ["r", "do_toggle_rewind"],
                        ["i", "do_toggle_info"],
                        ["l", "do_toggle_loop"],
                        ["j", "do_jump"],
                        ["o", "do_one"],
                        ["O", "do_one_back"],
                        ["t", "do_scroll_top"],
                        ["b", "do_scroll_bottom"],
                        ["m", "do_toggle_maxmin"],
                        ["/", "do_toggle_search"],
                    ])
                    .filter((k) => k[0].indexOf(r.ev.key) > -1)
                    .subscribe((k) => (func = k[1]));
            }
        } else if (r.ev.type == "click") {
            // no preventDefault, we want copy and paste !
            r["ev_type"] = "click";
            let tag = r.tag,
                ev = r.ev,
                el = r.ev.target;
            while (el) {
                cl = el.classList;
                cl.contains("fa-play")
                    ? (func = "do_toggle_play")
                    : cl.contains("fa-pause")
                    ? (func = "do_toggle_play")
                    : cl.contains("bar")
                    ? (func = "do_ctrl_seek")
                    : cl.contains("progress")
                    ? (func = "do_ctrl_seek")
                    : cl.contains("term_play_btn_big")
                    ? (func = "do_toggle_play")
                    : cl.contains("term_loop")
                    ? (func = "do_toggle_loop")
                    : cl.contains("term_rewind")
                    ? (func = "do_toggle_rewind")
                    : cl.contains("term_info")
                    ? (func = "do_toggle_info")
                    : cl.contains("term_maxmin")
                    ? (func = "do_toggle_maxmin")
                    : false;

                if (el == tag || func) break;
                el = el.parentElement;
            }
        }
        // thats the function realizing the intent:
        r.side_effect = func;
        log("user intent function: " + func);
        return r;
    }

    function reduce_user_input(ev) {
        // when its open we need to reduce everything entered
        // i.e. emit a stream of current text
        // plus we restrict the speed:
        return ((ev) => {
            ev.user_input = ev.target.value;
            return ev;
        }).filter((ev) => ev.user_input.length > 0);
        /* If its a textarea:
        // we remove duplicate lines and also not add lines with < 4 chars:
        .map(ev => {
            let lines = ev.target.value.replace(/\r\n/g,"\n").split("\n")
            let v = []
            stream.from(lines)
                .filter(line => line.length > 3)
                .distinct() // fockin_luvin_it
                .subscribe(line => v.push(line))
            ev.user_input = v
            return ev })
            */
    }

    /* ------------------------------------------------------------------------- *
     *                      VIDEO STREAM CREATION                                *
     * ------------------------------------------------------------------------- */
    let json_parse = (frame) => {
        try {
            f =  JSON.parse(frame)
        } catch {
            log("broken frame", frame)
            // insert an empty string and try parse the rest
            // but never happens up to now..
            debugger;
        }
        f[0] = parseInt(f[0] * 1000) // to millisecs
        return f
    }
                        
    function push_framesets(observer, tag) {
        /* nexting a bunch of frames if tag is playing.
         * No state set here, could be parallel to user intent
         * Actually not anymore, since we subscribe now to a combinattion of user
         * events and the framesets produced here => no collission possible.
         * But still its cleaner to not change the state here but in the subs only
         * */
        function foo(x) {
            debugger;

        }
        let data = tag.recording_data, frames, frame, frame_nr, match;
        stream
            .interval(tick_duration)
            .filter(
                (tick) =>
                tag.s.is_playing ||
                tag.s.do_one ||
                tag.s.jump_str ||
                tag.s.jump_time ||
                tag.s.jump_frame != false
            )
            .map((tick) => {
                /* push all frames until tag.s.cur_time + tick_duration */
                let frame_nr = tag.s.next_frame_nr;
                //if (frame_nr == 48) debugger
                if (frame_nr == 0) tag.term.reset();
                let to_time = tag.s.cur_time + tick_duration * 2 ** tag.s.play_speed;
                frames = [];

                add = (frame, frames) => {
                    frames.push(frame);
                    return 1;
                };

                while (frame_nr < data.length) {
                    s = ""; // total content string to search within
                    frame = data[frame_nr];
                    if (typeof frame == 'string') {
                        data[frame_nr] = frame = json_parse(frame)
                    }
                    if (tag.s.do_one) {
                        frame_nr += add(frame, frames);
                        break;
                    } else if (tag.s.jump_frame) {
                        frame_nr += add(frame, frames);
                        if (tag.s.jump_frame <= frame_nr) {
                            break;
                        }
                    } else if (tag.s.jump_str) {
                        frame_nr += add(frame, frames);
                        s = frame[2].length > 20 ? frame[2] : s + frame[2];
                        if (s.match(tag.s.jump_str)) {
                            // adding all frames to the next linebreak.
                            // to not stop at exactly at the match:
                            while (frame_nr < data.length && frame[2].indexOf("\n") == -1) {
                                frame = data[frame_nr];
                                frame_nr += add(frame, frames);
                            }
                            break;
                        }
                    } else if (tag.s.jump_time) {
                        if (frame[0] >= tag.s.jump_time) break;
                        frame_nr += add(frame, frames);
                    } else {
                        // normal playing
                        if (frame[0] >= tag.s.cur_time) break;
                        frame_nr += add(frame, frames);
                    }
                }
                //console.log('pushing', frame_nr, tag.s.cur_time, frames.length)
                observer.next({ tag: tag, frames: frames });
            })
            .subscribe((item) => 0);
    }

    /* ------------------------------------------------------------------------- *
     *                      VIDEO STREAM PLAYBACK (subscr. to main stream)       *
     * ------------------------------------------------------------------------- */
    function hilite_content(res) {
        let esc = String.fromCharCode(27);
        let color = esc + "[48;5;126m";
        let hilite = res.tag.s.jump_str || res.tag.s.hilite;
        if (!hilite) return res;
        let match = res.out.match(hilite);
        if (!match) return res;
        res.out = res.out.replace_all(match, color + match + esc + "[0m");
        return res;
    }

    function update_timer(r, tag) {
        let d = new Date(tag.s.cur_time).toUTCString().substr(17, 8);
        let n = tag.s.next_frame_nr,
            a = tag.recording_data.length;
        tag.sh_play_time.innerHTML = `<font size="-2">${n}/${a}</font> ${d}`;
    }

    do_play_frames = (r) => {
        /* writing the ansi frames to xterm2.js
         * the frames could be the result of a jump, one, ... operation, i.e. where
         * the player is not actually running
         * reminder: frames is an array of [content, timestamp] tuples
         * */
        //term.debug = true
        let tag = r.tag;
        //if (tag.s.jump_time) debugger
        stream
            .from(r.frames)
            .filter(frame => frame[1] != 'i')
            .reduce((out, frame) => out + frame[2], "")
            .map((out) => {
                return { tag: tag, out: out };
            })
            .map(hilite_content)
            .subscribe((res) => {
                tag.term.write(res.out);
                //tag.term.writeln('')
                // aaargh, the write is so async...
                //if (  tag.s.is_shot ) {
                //    tag.term.scrollDisp(1000)
                //    tag.term.scrollDisp(-5)
                //$('.term_wrap').trigger({type: 'keypress', which: 't'.codePointAt(0)})
            });
        tag.s.next_frame_nr += r.frames.length;
        //if (tag.s.next_frame_nr > 22) debugger
        update_timer(r, tag);
        let ts_old = tag.s.cur_time;
        tag.s.cur_time = ( tag.s.is_playing && ! tag.s.jump_time)
            ? ts_old + tick_duration * 2 ** tag.s.play_speed
            : r.frames[r.frames.length - 1][0]; // do_one, jump, search
        ctrl_update(tag)
        tag.s.do_one = false;

        if (tag.s.next_frame_nr > tag.recording_data.length-1) {
            reset(tag);
            tag.s.looping ? (tag.s.is_playing = true) : (tag.s.cast_ended = true);
        }
        if (tag.s.showing_preview) {
            reset(tag);
            tag.s.showing_preview = false;
        }
        tag.s.jump_frame = false;
        tag.s.jump_time = false;
        if (tag.s.jump_str) {
            tag.s.last_jump = tag.s.jump_str;
            tag.s.jump_str = false;
        }
    }

    total_time = (tag) => tag.recording_data[tag.recording_data.length-1] [0]
    pretty_time = (ts) => new Date(ts).toUTCString().substr(17, 8)

    ctrl_update = (tag) => {
        let cur = (tag.s.jump_time || tag.s.cur_time), t=total_time(tag)
        cur = Math.min(cur, t) // time continuously flows (ticks), independend of time stamps
        forall([['current', cur], ['total', t]], (k) => {
            get_elmt('play-' + k[0] + '-time', tag).innerText=pretty_time(k[1])})
        // progress bar
        let p = get_elmt('progress', tag)
        let tw=width(p)
        get_elmt('bar', p).style.width = (cur / t * tw) + 'px'
        p = get_elmt("play-pause", tag)
        tag.s.is_playing ? tw = ['fa-play', 'fa-pause'] : tw=['fa-pause', 'fa-play']
        p.children[0].classList.remove(tw[0])
        p.children[0].classList.add(tw[1])
    }

    const do_ctrl_seek = (tag, r) => {
        let b = get_elmt('progress', tag)
        let x = r.ev.offsetX
        let ts = x / width(b) * total_time(tag) 
        let op = tag.s.is_playing
        reset(tag);
        tag.s.is_playing = op
        tag.s.jump_time = ts
    }

    /* ------------------------------------------------------------------------- *
     *                      DOM STREAM TAG CREATION
     * ------------------------------------------------------------------------- */
    function set_scrolls(tag, attr_name, to_tag) {
        to_tag.style.overflow = "hidden";
        let os = attr(attr_name, tag, "");
        let i = os.length;
        while (i--) to_tag.style["overflow-" + os.charAt(i)] = "scroll";
    }


    function run_main_stream(tag, init_intent) {
        is_text_input  = (ev) => ev.target.classList.contains('has_user_input')
        key_up$ = stream.fromEvent(tag, "keyup");
        esc$ = key_up$.filter((ev) => ev.key == "Escape");
        // Esc has no keydown
        user_text_inp$ = key_up$
            .filter(is_text_input)
            .filter((ev) => ev.key != "/") // opens search
            .filter((ev) => ev.key != "Escape")
            .filter((ev) => ev.key != "Meta")
            .map((ev) => {
                debugger
                ev.user_input = ev.target.value;
                return ev;
            })
        // 0 -> we search every character:
            .filter((ev) => ev.user_input.length > 0);
        // 2021: this was keydown but Rx does not fire anymore an keydown
        user_ctrl_key$ = stream
            .fromEvent(tag, "keyup")
            .map(log)
            .filter((ev) => ev.key != "Meta")
            .filter((ev) => !is_text_input(ev))
            .map((ev) => {
                console.log("control key", ev.key)
                return ev
            });

        user_intent$ = stream
            .fromEvent(tag, "click")
            .merge(user_text_inp$)
            .merge(user_ctrl_key$)
            .merge(esc$)
            .map((ev) => {
                return { tag: tag, ev: ev };
            })
            .map(add_intent_function);

        stream
            .create((o) => push_framesets(o, tag))
            .merge(stream.from(init_intent))
            .merge(user_intent$)
            .map((item) => (dbg_stream ? log(item) : item))
            .map((item) => {
                if (dbg_store) log(JSON.stringify(item.tag.s, null));
                return item;
            })
            .subscribe((r) => {
                r.frames
                    ? do_play_frames(r) // paint a bunch of frames
                    : dispatch_intent_function(r); // realize user intent

                if (r.ev || r.tag.s.cast_ended) {
                    do_update_controls_view(tag);
                    ctrl_update(tag)
                }
            });
    }

    function fetch_term_raw(url, callback) {
        fetch(url)
            .then((response) => response.text())
            .then((data) => callback(null, data, url))
            .catch((error) => callback(error, null, url));
    }
    
    function to_tc_format(tag, data) {
        /* to corect format [{meta..}, frame1, frame2] */
        let m = {}
        function complete_meta_with_tag_attrs(tag, m, data) {
            function i(s) { return parseInt(s); }
            m.by = attr("by", tag, m.by || 'anon') 
            // rows, cols: terminal size. el_rows = widget size
            // it makes no sense to change the term rows/cols by tag attrs, will screw ansi
            // only restrict viewport
            m.el_rows = i(attr("rows", tag, m.rows || dflt_rows))
            m.el_cols = i(attr("cols", tag, m.cols || dflt_cols) )
            m.rows = i(m.rows || dflt_rows)
            m.cols = i(m.cols || dflt_cols)
            m.kB ? kb = ", ${meta.kB} kB (uncompressed)" : kb = ''
            try{
                ts = i(attr("ts", tag, m.ts || 0))
            } catch {
                ts =0
            }
            ts ? ts=(new Date(ts * 1000) + ', ') : ts = ''
            m.metadata_html = `<font size="-2">
                ${ts}${m.by}, ${m.rows}rows x ${m.cols} columns${kb}</font>`;
        }
        if (!data) return ['No data']
        if (data[0] == '{') {
            log('Is asciicinema v2') // e.g. just redirected into file
            strct = data.split(/\r?\n/);
            // last line empty?
            while (strct[strct.length-1][0] != '[') strct.pop()
            // meta:
            strct[0] = m = JSON.parse(strct[0])
            // our legacy names #TODO
            m.rows = m.height
            m.cols = m.width
            m.ts = m.timestamp
        }
        else if (data[0] != '[') {
            log('Is raw data') // e.g. just redirected into file
            strct = [m, data]
        } else {
            log('Is tc legacy data') // e.g. just redirected into file
            strct = JSON.parse(data)
            m = strct[0]
            for (i = 1; i < strct.length; i++) strct[i] = [strct[i][1], 'o', eval(strct[i][0])]
        }
        complete_meta_with_tag_attrs(tag, m, data)
        strct.shift()
        return [0, m, strct]
    }

    function setup_loaded_termcast_tag(tag, data) {
        /* setting up the terminal tag after page load.  The tag itself is our
         * global store for state which we may only change before the event stream
         * and in its subscription */
        tag.term = new Terminal();
        tag.innerHTML = tag_html("loaded", tag);

        let term_el = by_tag_name("terminal", tag)[0];
        let term_wrap = get_elmt("term_wrap", tag);
        set_scrolls(tag, "outer_scrolls", term_wrap);
        let rec = to_tc_format(tag, data);
        let err = rec.shift()
        if (err) { tag.innerHTML = err; return; }
        let meta = rec.shift()
        rec = rec[0]
        tag.recording_data = rec;
        // last one for total time required to be parsed rite now
        rec[rec.length-1] = json_parse(rec[rec.length-1])

        tag.term.open(term_el, (focus = true));

        //
        //   tag.term.insertMode = true
        //   tag.term.applicationCursor = true
        //   tag.term.applicationKeypad = true
        //   tag.term.cursorBlink = true
        //   tag.term.screenKeys = true
        //   tag.term.userScrolling = true
        //   tag.term.flowControl = true
        //   tag.term.useFlowControl = true

        // TODO
        // let drags = by_cls_name("draggable", tag);
        // for (i = 0; i < drags.length; i++) drag_and_drop(drags[i]);
        // tag.s: it's state
        // first item of the json is the meta definitions (rows, colors, kb, ...)
        tag.s.recorder_rows = meta.rows;
        tag.s.recorder_cols = meta.cols;
        get_elmt("term_meta", tag).innerHTML = meta.metadata_html;
        tag.term.resize(meta.cols, meta.rows);

        // if (rec.length > 1) {
        //     let x = rec[rec.length - 1][0];
        //     if (x.endsWith("exit\\r\\n'")) rec.pop();
        // }

        // shots have no timing information:
        tag.s.is_shot = false;
        //if (Number.isInteger(rec[0][1])) {
        //    // conversion of all escape chars, better do only once:
        //    for (i = 0; i < rec.length; i++) rec[i][0] = eval(rec[i][0]);
        //} else {
        //    // screenshot only:
        //    tag.s.is_shot = true;
        //    // if we did  video and want a shot later we just change the
        //    // first frame's timing to a non Integer, so we land here.
        //    // Then we must convert the first items to shot format w/o timings:
        //    if (rec[0].length == 2) {
        //        for (i = 0; i < rec.length; i++) rec[i] = rec[i][0];
        //    }
        //    // normal shot format: No timings:
        //    debugger;
        //    //for (i = 0; i < rec.length; i++) rec[i] = [eval(rec[i]), 1];
        //    //get_elmt("term_controls", tag).style.visibility = "hidden";
        //}

        /*let big_btn = get_elmt("term_play_btn_big", tag);
        big_btn.style.top = (height(term_wrap) - height(big_btn)) / 2 + "px";
        big_btn.style.left = (width(term_wrap) - width(big_btn)) / 2 + "px";
        */

        reset(tag);
        tag.s.play_speed = parseInt(attr("play_speed", tag, 0)); // 2 ** this

        let hilite = attr("hilite", tag);
        let jump_str = attr("jump_str", tag);
        jump_str = jump_str ? jump_str : hilite;
        tag.s.hilite = hilite ? new RegExp(hilite) : "";
        tag.s.jump_str = jump_str ? new RegExp(jump_str) : "";
        tag.s.jump_time = false

        // jump to first occurrance of this. jump != hilitie in general
        let jt = attr("jump_frame", tag);

        init_intent = [];

        if (jt > 0) {
            tag.s.jump_frame = jt;
        } else if (tag.s.is_shot) {
            tag.s.is_playing = true;
            // TODO can't work as init intent, we have then not yet frames on the
            // screen:
            init_intent.push({ tag: tag, side_effect: "do_scroll_top" });
            tag.s.scroll = "top";
            tag.term.scrollDisp(1000);
            // go back (exits)
            tag.term.scrollDisp(-5);
        } else {
            tag.s.jump_frame = false;
            if (tag.s.jump_str || tag.s.jump_frame) tag.s.showing_preview = true;
        }

        if (tag.hasAttribute("autoplay")) {
            tag.s.showing_preview = false;
            tag.s.is_playing = true;
        }
        if (tag.hasAttribute("looping")) {
            tag.s.showing_preview = false;
            tag.s.is_playing = true;
            tag.s.looping = true;
        }

        //style the inner terminal:
        let xt = by_cls_name("xterm-viewport", tag)[0];
        xt.style["background-color"] = attr("inner_bgcol", tag, "black");
        set_scrolls(tag, "inner_scrolls", xt);

        tag.sh_play_time = get_elmt("term_timer", tag);
        tag.term.textarea.focus();
        //tag.term.linkifier._linkMatchers = [];

        do_update_controls_view(tag);
        run_main_stream(tag, init_intent);
    }

    // ---------------------------------------------------------------------assets:
    get_help_table = () => {
        let ht = `
    <table style="font-size: 10px">
        <tr><td colspan="4"><span class="term_meta"></span></td></tr>

        <tr><td>!p         </td> <td> Toggle !Play / !Pause                               </td>
            <td>!q         </td> <td> !Quit Play                                          </td></tr>
        <tr><td>!l         </td> <td> Toggle !Looping Playback                            </td>
            <td>!s, !d, !f </td> <td> !Slower / !Default / !Faster Playback Speed         </td></tr>
        <tr><td>!m         </td> <td> Toggle !Maximize / !Minimize. Starts if not running </td>
            <td>!r         </td> <td> !Rewind                                             </td></tr>
        <tr><td>!o/(!O)    </td> <td> !One frame (back) at a time                         </td>
            <td>!t/!b      </td> <td> Scroll to !Top or !Bottom                           </td></tr>
        <tr><td>!i         </td> <td> Toggle This !Info                                   </td>
            <td>!/         </td> <td> Search substring                                    </td></tr>
        <tr><td>!j         </td> <td> !Jump to next occurrance of search word             </td>
            <td>!ESC       </td> <td> Close all popups                                    </td></tr>

    </table>`;
        // 'foo !abar' => 'foo <b>a</b>bar'
        let s = "";
        stream
            .from(ht.split("!"))
            .map((part, i) => {
                if (i == 0) return part;
                return "<b>" + part[0] + "</b>" + part.substring(1);
            })
            .subscribe((i) => (s += i));
        return s;
    };

    function setup_termcast_tag(tag) {
        /* add the player icons, register an observable data stream */
        log("setting up termcast tag", tag);
        tag.s = {}; // the global state, like a redux store
        let src = attr("content", tag);
        if (!src && tag.innerText) src = tag.innerHTML.trim();
        if (!src) src = tag.recording_data;
        if (src) {
            setup_loaded_termcast_tag(tag, src);
        } else {
            tag.innerHTML = tag_html("loading", tag);
            let src = attr("src", tag);
            function run_fetched(err, data) {
                if (err) {
                    log(err);
                    return;
                }
                setup_loaded_termcast_tag(tag, data);
            }
            fetch_term_raw(src, run_fetched);
        }
        return tag;
    }

    function set_control_fade_in_out(el) {
        let h='hidden', v='visible'
        let s = (k) => el.addEventListener(k[0], (ev) => {
            let c=by_cls_name('controls', el)[0].classList
            c.remove(k[1]); c.add(k[2])
        })
        forall([['mouseenter', h, v], ['mouseleave', v, h]], s)
    }
    forall(by_tag_name("termcast"), set_control_fade_in_out)

    window.TermCast = {
        all_casts: all_casts,
        forall: forall,
        setup_termcast_tag: setup_termcast_tag,
    };
    by_tag_name
}

define_termcasts(window, document);
var TC = window.TermCast 
window.addEventListener("load", () => TC.forall(TC.all_casts(), TC.setup_termcast_tag));


