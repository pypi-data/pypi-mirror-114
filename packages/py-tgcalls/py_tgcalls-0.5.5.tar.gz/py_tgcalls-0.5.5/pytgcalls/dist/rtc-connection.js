"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// @ts-ignore
const node_fetch_1 = require("node-fetch");
const tgcalls_1 = require("./tgcalls");
class RTCConnection {
    constructor(chat_id, file_path, port, bitrate, logMode, buffer_lenght, invite_hash) {
        this.chat_id = chat_id;
        this.file_path = file_path;
        this.port = port;
        this.bitrate = bitrate;
        this.logMode = logMode;
        this.buffer_lenght = buffer_lenght;
        this.invite_hash = invite_hash;
        this.tgcalls = new tgcalls_1.TGCalls({}, chat_id);
        this.stream = new tgcalls_1.Stream(file_path, 16, bitrate, 1, logMode, buffer_lenght);
        this.tgcalls.joinVoiceCall = async (payload) => {
            payload = {
                chat_id: this.chat_id,
                ufrag: payload.ufrag,
                pwd: payload.pwd,
                hash: payload.hash,
                setup: payload.setup,
                fingerprint: payload.fingerprint,
                source: payload.source,
                invite_hash: this.invite_hash,
            };
            if (logMode > 0) {
                console.log('callJoinPayload -> ', payload);
            }
            const joinCallResult = await (await node_fetch_1.default(`http://localhost:${this.port}/request_join_call`, {
                method: 'POST',
                body: JSON.stringify(payload),
            })).json();
            if (logMode > 0) {
                console.log('joinCallRequestResult -> ', joinCallResult);
            }
            return joinCallResult;
        };
        this.stream.on('finish', async () => {
            await node_fetch_1.default(`http://localhost:${this.port}/ended_stream`, {
                method: 'POST',
                body: JSON.stringify({
                    chat_id: chat_id,
                }),
            });
        });
    }
    async joinCall() {
        try {
            return await this.tgcalls.start(this.stream.createTrack());
        }
        catch (e) {
            this.stream.stop();
            if (this.logMode > 0) {
                console.log('joinCallError ->', e);
            }
            return false;
        }
    }
    stop() {
        try {
            this.stream.stop();
            this.tgcalls.close();
        }
        catch (e) { }
    }
    async leave_call() {
        try {
            this.stop();
            return await (await node_fetch_1.default(`http://localhost:${this.port}/request_leave_call`, {
                method: 'POST',
                body: JSON.stringify({
                    chat_id: this.chat_id,
                }),
            })).json();
        }
        catch (e) {
            return {
                action: 'REQUEST_ERROR',
                message: e.toString(),
            };
        }
    }
    pause() {
        this.stream.pause();
    }
    async resume() {
        this.stream.resume();
    }
    changeStream(file_path) {
        this.stream.setReadable(file_path);
    }
}
exports.default = RTCConnection;
