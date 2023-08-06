// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Signal } from '@lumino/signaling';
const TRANSIENT_CELL_CLASS = 'jp-CodeConsole-transientCell';
/**
 * A handler for capturing API messages from other sessions that should be
 * rendered in a given parent.
 */
export class TransientHandler {
    /**
     * Construct a new transient message handler.
     */
    constructor(options) {
        this._enabled = true;
        this._isDisposed = false;
        this.sessionContext = options.sessionContext;
        this.sessionContext.iopubMessage.connect(this.onIOPubMessage, this);
        this._parent = options.parent;
    }
    /**
     * Set whether the handler is able to inject transient cells into a console.
     */
    get enabled() {
        return this._enabled;
    }
    set enabled(value) {
        this._enabled = value;
    }
    /**
     * The transient handler's parent receiver.
     */
    get parent() {
        return this._parent;
    }
    /**
     * Test whether the handler is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the resources held by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        Signal.clearData(this);
    }
    /**
     * Handler IOPub messages.
     *
     * @returns `true` if the message resulted in a new cell injection or a
     * previously injected cell being updated and `false` for all other messages.
     */
    onIOPubMessage(sender, msg) {
        var _a;
        // Only process messages if Transient cell injection is enabled.
        if (!this._enabled) {
            return false;
        }
        let kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return false;
        }
        // Check whether this message came from an external session.
        let parent = this._parent;
        let session = msg.parent_header.session;
        if (session === kernel.clientId) {
            return false;
        }
        let msgType = msg.header.msg_type;
        if (msgType !== 'transient_display_data') {
            return false;
        }
        let parentHeader = msg.parent_header;
        let parentMsgId = parentHeader.msg_id;
        let cell;
        cell = this._parent.getCell(parentMsgId);
        if (!cell) {
            // if not cell with the same parentMsgId, create a dedicated cell
            cell = this._newCell(parentMsgId);
        }
        let output = msg.content;
        output.output_type = 'display_data';
        cell.model.outputs.add(output);
        parent.update();
        return true;
    }
    /**
     * Create a new code cell for an input originated from a transient session.
     */
    _newCell(parentMsgId) {
        let cell = this.parent.createCodeCell();
        cell.addClass(TRANSIENT_CELL_CLASS);
        this._parent.addCell(cell, parentMsgId);
        return cell;
    }
}
//# sourceMappingURL=transient.js.map