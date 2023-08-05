"use strict";
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, state, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
};
var __classPrivateFieldSet = (this && this.__classPrivateFieldSet) || function (receiver, state, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return (kind === "a" ? f.call(receiver, value) : f ? f.value = value : state.set(receiver, value)), value;
};
var _SdpBuilder_lines, _SdpBuilder_newLine;
Object.defineProperty(exports, "__esModule", { value: true });
exports.SdpBuilder = void 0;
class SdpBuilder {
    constructor() {
        _SdpBuilder_lines.set(this, []);
        _SdpBuilder_newLine.set(this, []);
    }
    get lines() {
        return __classPrivateFieldGet(this, _SdpBuilder_lines, "f").slice();
    }
    join() {
        return __classPrivateFieldGet(this, _SdpBuilder_lines, "f").join('\n');
    }
    finalize() {
        return this.join() + '\n';
    }
    add(line) {
        __classPrivateFieldGet(this, _SdpBuilder_lines, "f").push(line);
    }
    push(word) {
        __classPrivateFieldGet(this, _SdpBuilder_newLine, "f").push(word);
    }
    addJoined(separator = '') {
        this.add(__classPrivateFieldGet(this, _SdpBuilder_newLine, "f").join(separator));
        __classPrivateFieldSet(this, _SdpBuilder_newLine, [], "f");
    }
    addCandidate(c) {
        this.push('a=candidate:');
        this.push(`${c.foundation} ${c.component} ${c.protocol} ${c.priority} ${c.ip} ${c.port} typ ${c.type}`);
        this.push(` generation ${c.generation}`);
        this.addJoined();
    }
    addHeader(session_id, ssrcs) {
        this.add('v=0');
        this.add(`o=- ${session_id} 2 IN IP4 0.0.0.0`);
        this.add('s=-');
        this.add('t=0 0');
        this.add(`a=group:BUNDLE ${ssrcs.map(this.toAudioSsrc).join(' ')}`);
        this.add('a=ice-lite');
    }
    addTransport(transport) {
        this.add(`a=ice-ufrag:${transport.ufrag}`);
        this.add(`a=ice-pwd:${transport.pwd}`);
        for (let fingerprint of transport.fingerprints) {
            this.add(`a=fingerprint:${fingerprint.hash} ${fingerprint.fingerprint}`);
            this.add(`a=setup:passive`);
        }
        let candidates = transport.candidates;
        for (let candidate of candidates) {
            this.addCandidate(candidate);
        }
    }
    addSsrcEntry(entry, transport, isAnswer) {
        let ssrc = entry.ssrc;
        this.add(`m=audio ${entry.isMain ? 1 : 0} RTP/SAVPF 111 126`);
        if (entry.isMain) {
            this.add('c=IN IP4 0.0.0.0');
        }
        this.add(`a=mid:${this.toAudioSsrc(entry)}`);
        if (entry.isRemoved) {
            this.add('a=inactive');
            return;
        }
        if (entry.isMain) {
            this.addTransport(transport);
        }
        this.add('a=rtpmap:111 opus/48000/2');
        this.add('a=rtpmap:126 telephone-event/8000');
        this.add('a=fmtp:111 minptime=10; useinbandfec=1; usedtx=1');
        this.add('a=rtcp:1 IN IP4 0.0.0.0');
        this.add('a=rtcp-mux');
        this.add('a=rtcp-fb:111 transport-cc');
        this.add('a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level');
        if (isAnswer) {
            this.add('a=recvonly');
            return;
        }
        else if (entry.isMain) {
            this.add('a=sendrecv');
        }
        else {
            this.add('a=sendonly');
            this.add('a=bundle-only');
        }
        this.add(`a=ssrc-group:FID ${ssrc}`);
        this.add(`a=ssrc:${ssrc} cname:stream${ssrc}`);
        this.add(`a=ssrc:${ssrc} msid:stream${ssrc} audio${ssrc}`);
        this.add(`a=ssrc:${ssrc} mslabel:audio${ssrc}`);
        this.add(`a=ssrc:${ssrc} label:audio${ssrc}`);
    }
    addConference(conference, isAnswer = false) {
        let ssrcs = conference.ssrcs;
        if (isAnswer) {
            for (let ssrc of ssrcs) {
                if (ssrc.isMain) {
                    ssrcs = [ssrc];
                    break;
                }
            }
        }
        this.addHeader(conference.session_id, ssrcs);
        for (let entry of ssrcs) {
            this.addSsrcEntry(entry, conference.transport, isAnswer);
        }
    }
    static fromConference(conference, isAnswer = false) {
        const sdp = new SdpBuilder();
        sdp.addConference(conference, isAnswer);
        return sdp.finalize();
    }
    toAudioSsrc(ssrc) {
        if (ssrc.isMain) {
            return '0';
        }
        return `audio${ssrc.ssrc}`;
    }
}
exports.SdpBuilder = SdpBuilder;
_SdpBuilder_lines = new WeakMap(), _SdpBuilder_newLine = new WeakMap();
