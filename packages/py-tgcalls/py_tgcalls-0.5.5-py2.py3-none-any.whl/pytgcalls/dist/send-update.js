"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// @ts-ignore
const node_fetch_1 = require("node-fetch");
exports.default = async (port, params) => {
    await node_fetch_1.default(`http://localhost:${port}/update_request`, {
        method: 'POST',
        body: JSON.stringify(params),
    });
};
