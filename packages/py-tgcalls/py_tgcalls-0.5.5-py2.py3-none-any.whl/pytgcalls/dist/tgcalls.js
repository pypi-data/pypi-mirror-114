"use strict";
var __classPrivateFieldSet = (this && this.__classPrivateFieldSet) || function (receiver, state, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return (kind === "a" ? f.call(receiver, value) : f ? f.value = value : state.set(receiver, value)), value;
};
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, state, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
};
var _TGCalls_connection, _TGCalls_params, _TGCalls_chat_id;
Object.defineProperty(exports, "__esModule", { value: true });
exports.TGCalls = exports.Stream = void 0;
const events_1 = require("events");
const wrtc_1 = require("wrtc");
const sdp_builder_1 = require("./sdp-builder");
const utils_1 = require("./utils");
var stream_1 = require("./stream");
Object.defineProperty(exports, "Stream", { enumerable: true, get: function () { return stream_1.Stream; } });
class TGCalls extends events_1.EventEmitter {
    constructor(params, chat_id) {
        super();
        _TGCalls_connection.set(this, void 0);
        _TGCalls_params.set(this, void 0);
        _TGCalls_chat_id.set(this, void 0);
        __classPrivateFieldSet(this, _TGCalls_chat_id, chat_id, "f");
        __classPrivateFieldSet(this, _TGCalls_params, params, "f");
    }
    async start(track) {
        if (__classPrivateFieldGet(this, _TGCalls_connection, "f")) {
            throw new Error('Connection already started');
        }
        else if (!this.joinVoiceCall) {
            throw new Error('Please set the `joinVoiceCall` callback before calling `start()`');
        }
        __classPrivateFieldSet(this, _TGCalls_connection, new wrtc_1.RTCPeerConnection(), "f");
        __classPrivateFieldGet(this, _TGCalls_connection, "f").oniceconnectionstatechange = async () => {
            var _a, _b;
            this.emit('iceConnectionState', (_a = __classPrivateFieldGet(this, _TGCalls_connection, "f")) === null || _a === void 0 ? void 0 : _a.iceConnectionState);
            switch ((_b = __classPrivateFieldGet(this, _TGCalls_connection, "f")) === null || _b === void 0 ? void 0 : _b.iceConnectionState) {
                case 'closed':
                case 'failed':
                    this.emit('hangUp');
                    break;
            }
        };
        __classPrivateFieldGet(this, _TGCalls_connection, "f").addTrack(track);
        const offer = await __classPrivateFieldGet(this, _TGCalls_connection, "f").createOffer({
            offerToReceiveVideo: false,
            offerToReceiveAudio: true,
        });
        await __classPrivateFieldGet(this, _TGCalls_connection, "f").setLocalDescription(offer);
        if (!offer.sdp) {
            return false;
        }
        const { ufrag, pwd, hash, fingerprint, source } = utils_1.parseSdp(offer.sdp);
        if (!ufrag || !pwd || !hash || !fingerprint || !source) {
            return false;
        }
        let joinGroupCallResult;
        try {
            joinGroupCallResult = await this.joinVoiceCall({
                ufrag,
                pwd,
                hash,
                setup: 'active',
                fingerprint,
                source,
                params: __classPrivateFieldGet(this, _TGCalls_params, "f"),
            });
        }
        catch (error) {
            __classPrivateFieldGet(this, _TGCalls_connection, "f").close();
            throw error;
        }
        if (!joinGroupCallResult || !joinGroupCallResult.transport) {
            __classPrivateFieldGet(this, _TGCalls_connection, "f").close();
            // @ts-ignore
            throw new Error('No active voice chat found on ' + __classPrivateFieldGet(this, _TGCalls_chat_id, "f"));
        }
        const session_id = Date.now();
        const conference = {
            session_id,
            transport: joinGroupCallResult.transport,
            ssrcs: [{ ssrc: source, isMain: true }],
        };
        await __classPrivateFieldGet(this, _TGCalls_connection, "f").setRemoteDescription({
            type: 'answer',
            sdp: sdp_builder_1.SdpBuilder.fromConference(conference, true),
        });
        return true;
    }
    close() {
        var _a;
        (_a = __classPrivateFieldGet(this, _TGCalls_connection, "f")) === null || _a === void 0 ? void 0 : _a.close();
        __classPrivateFieldSet(this, _TGCalls_connection, undefined, "f");
    }
}
exports.TGCalls = TGCalls;
_TGCalls_connection = new WeakMap(), _TGCalls_params = new WeakMap(), _TGCalls_chat_id = new WeakMap();
