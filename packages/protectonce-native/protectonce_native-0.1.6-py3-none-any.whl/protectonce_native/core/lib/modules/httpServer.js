const uuid = require('uuid');
const ProtectOnceContext = require('./context');
const Logger = require('../utils/logger');

function createSession() {
    // TODO: This is a stopgap implementation of session id
    const sessionId = uuid.v4();
    ProtectOnceContext.create(sessionId, {});

    Logger.write(Logger.DEBUG && `httpServer: Session created with session id: ${sessionId}`);
    return sessionId;
}

/**
 * Releases the stored http session, this should be called when a request is completed
 * @param  {Object} sessionData The incoming data is of the form:
 *          @param {Object} data This holds following field:
 *              @param {String} poSessionId
 */
function releaseSession(sessionData) {
    try {
        ProtectOnceContext.release(sessionData.data.poSessionId);
        Logger.write(Logger.DEBUG && `httpServer: Releasing data for session id: ${sessionData.data.poSessionId}`);
    } catch (e) {
        Logger.write(Logger.DEBUG && `httpServer: Failed to release data`);
    }
}

/**
 * Stores the http request info in the session context
 * @param  {Object} requestData The incoming data is of the form:
 *          @param {Object} data This holds http request object of the form:
 *              @param {Object} queryParams
 *              @param {Object} headers
 *              @param {String} method
 *              @param {String} path
 *              @param {String} sourceIP
 *              @param {String} poSessionId
 */
function storeHttpRequestInfo(requestData) {
    try {
        ProtectOnceContext.update(requestData.data.poSessionId, requestData.data);
        Logger.write(Logger.DEBUG && `httpServer: Updated data for session id: ${sessionData.data.poSessionId}`);
    } catch (e) {
        Logger.write(Logger.DEBUG && `httpServer: Failed to store session data`);
    }
}

function scanHeaders() {
    // TODO: Implement this
    return {
        'blocked': false
    }
}

function scanHttpData() {
    // TODO: Not Implemented
    return {
        'blocked': false
    }
}

module.exports = {
    createSession: createSession,
    releaseSession: releaseSession,
    storeHttpRequestInfo: storeHttpRequestInfo,
    scanHeaders: scanHeaders,
    scanHttpData: scanHttpData
};
