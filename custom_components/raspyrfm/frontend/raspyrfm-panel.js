const { LitElement, html, css } = window;

class RaspyRFMPanel extends LitElement {
  static get properties() {
    return {
      hass: {},
      learning: { type: Boolean },
      signals: { state: true },
      devices: { state: true },
      formType: { state: true },
      formName: { state: true },
      formOn: { state: true },
      formOff: { state: true },
      formTrigger: { state: true },
      error: { state: true },
    };
  }

  static get styles() {
    return css`
      :host {
        display: block;
        padding: 24px;
      }
      .actions {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
      }
      ha-card {
        margin-bottom: 16px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th, td {
        padding: 8px;
        border-bottom: 1px solid var(--divider-color);
      }
      .signal-list {
        max-height: 300px;
        overflow-y: auto;
      }
      .signal-entry {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px;
        border-bottom: 1px solid var(--divider-color);
      }
      .signal-entry:last-child {
        border-bottom: none;
      }
      .signal-meta {
        font-size: 12px;
        color: var(--secondary-text-color);
      }
      .form-grid {
        display: grid;
        gap: 12px;
      }
      .form-row {
        display: flex;
        gap: 12px;
        align-items: center;
      }
      .pill {
        padding: 2px 8px;
        border-radius: 12px;
        background-color: var(--accent-color);
        color: var(--text-primary-color);
        font-size: 12px;
      }
      .error {
        color: var(--error-color);
        margin-bottom: 12px;
      }
    `;
  }

  constructor() {
    super();
    this.learning = false;
    this.signals = [];
    this.devices = [];
    this.formType = "switch";
    this.formName = "";
    this.formOn = null;
    this.formOff = null;
    this.formTrigger = null;
    this.error = null;
    this._signalUnsub = null;
    this._learningUnsub = null;
  }

  connectedCallback() {
    super.connectedCallback();
    this._initialize();
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    if (this._signalUnsub) {
      this._signalUnsub();
      this._signalUnsub = null;
    }
    if (this._learningUnsub) {
      this._learningUnsub();
      this._learningUnsub = null;
    }
  }

  async _initialize() {
    await this._loadState();
    await this._subscribeSignals();
    await this._subscribeLearning();
    await this._refreshDevices();
  }

  async _loadState() {
    const status = await this.hass.callWS({ type: "raspyrfm/learning/status" });
    this.learning = status.active;
    const signals = await this.hass.callWS({ type: "raspyrfm/signals/list" });
    this.signals = signals.signals || [];
  }

  async _subscribeSignals() {
    this._signalUnsub = await this.hass.connection.subscribeMessage((message) => {
      if (message.type !== "event") {
        return;
      }
      const signal = message.event;
      this.signals = [...this.signals, signal];
    }, {
      type: "raspyrfm/signals/subscribe"
    });
  }

  async _subscribeLearning() {
    this._learningUnsub = await this.hass.connection.subscribeMessage((message) => {
      if (message.type !== "event") {
        return;
      }
      this.learning = message.event.active;
    }, {
      type: "raspyrfm/learning/subscribe"
    });
  }

  async _refreshDevices() {
    const response = await this.hass.callWS({ type: "raspyrfm/devices/list" });
    this.devices = response.devices || [];
  }

  render() {
    return html`
      <div class="actions">
        <mwc-button raised @click=${this._handleStartLearning} ?disabled=${this.learning}>Start learning</mwc-button>
        <mwc-button @click=${this._handleStopLearning} ?disabled=${!this.learning}>Stop learning</mwc-button>
        <mwc-button @click=${this._refreshDevices}>Refresh devices</mwc-button>
      </div>
      ${this.error ? html`<div class="error">${this.error}</div>` : ""}
      ${this._renderSignals()}
      ${this._renderForm()}
      ${this._renderDevices()}
    `;
  }

  _renderSignals() {
    if (!this.signals.length) {
      return html`
        <ha-card header="Captured signals">
          <div class="card-content">No signals received yet. Use the start learning button and trigger your remotes or sensors.</div>
        </ha-card>
      `;
    }
    return html`
      <ha-card header="Captured signals">
        <div class="card-content signal-list">
          ${this.signals.map((signal) => this._renderSignal(signal))}
        </div>
      </ha-card>
    `;
  }

  _renderSignal(signal) {
    return html`
      <div class="signal-entry">
        <div>
          <div>${signal.payload}</div>
          <div class="signal-meta">${signal.received}</div>
        </div>
        <div class="form-row">
          <mwc-button dense @click=${() => this._selectSignal(signal.payload, "on")}>Set as ON</mwc-button>
          <mwc-button dense @click=${() => this._selectSignal(signal.payload, "off")}>Set as OFF</mwc-button>
          <mwc-button dense @click=${() => this._selectSignal(signal.payload, "trigger")}>Set as trigger</mwc-button>
        </div>
      </div>
    `;
  }

  _renderForm() {
    return html`
      <ha-card header="Create Home Assistant device">
        <div class="card-content form-grid">
          <div class="form-row">
            <ha-textfield label="Name" .value=${this.formName} @input=${(ev) => this._updateName(ev.target.value)}></ha-textfield>
            <ha-select label="Type" .value=${this.formType} @selected=${(ev) => this._updateType(ev.target.value)}>
              <mwc-list-item value="switch">Switch</mwc-list-item>
              <mwc-list-item value="binary_sensor">Binary sensor</mwc-list-item>
            </ha-select>
          </div>
          ${this.formType === "switch"
            ? html`
                <div class="form-row">
                  <span class="pill">ON</span>
                  <span>${this.formOn || "Choose a captured signal"}</span>
                </div>
                <div class="form-row">
                  <span class="pill">OFF</span>
                  <span>${this.formOff || "Optional"}</span>
                </div>
              `
            : html`
                <div class="form-row">
                  <span class="pill">Trigger</span>
                  <span>${this.formTrigger || "Choose a captured signal"}</span>
                </div>
              `}
          <div>
            <mwc-button raised @click=${this._createDevice}>Create device</mwc-button>
          </div>
        </div>
      </ha-card>
    `;
  }

  _renderDevices() {
    if (!this.devices.length) {
      return html`
        <ha-card header="Configured devices">
          <div class="card-content">No RaspyRFM devices created yet.</div>
        </ha-card>
      `;
    }
    return html`
      <ha-card header="Configured devices">
        <div class="card-content">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Signals</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              ${this.devices.map((device) => html`
                <tr>
                  <td>${device.name}</td>
                  <td>${device.device_type}</td>
                  <td>
                    ${Object.entries(device.signals || {}).map(([key, value]) => html`<div><strong>${key}</strong>: ${value}</div>`) }
                  </td>
                  <td>
                    <mwc-button @click=${() => this._deleteDevice(device.device_id)}>Delete</mwc-button>
                  </td>
                </tr>
              `)}
            </tbody>
          </table>
        </div>
      </ha-card>
    `;
  }

  _updateName(value) {
    this.formName = value;
  }

  _updateType(value) {
    this.formType = value;
  }

  _selectSignal(payload, target) {
    if (this.formType === "switch") {
      if (target === "on") {
        this.formOn = payload;
      } else if (target === "off") {
        this.formOff = payload;
      } else {
        this.error = "Switches do not use trigger signals";
        return;
      }
    } else {
      this.formTrigger = payload;
    }
    this.error = null;
    this.requestUpdate();
  }

  async _createDevice() {
    this.error = null;
    const name = this.formName.trim();
    if (!name) {
      this.error = "Please provide a device name.";
      return;
    }

    const signals = {};
    if (this.formType === "switch") {
      if (!this.formOn) {
        this.error = "Select an ON signal for the switch.";
        return;
      }
      signals.on = this.formOn;
      if (this.formOff) {
        signals.off = this.formOff;
      }
    } else {
      if (!this.formTrigger) {
        this.error = "Select a trigger signal for the sensor.";
        return;
      }
      signals.trigger = this.formTrigger;
    }

    try {
      await this.hass.callWS({
        type: "raspyrfm/device/create",
        name,
        device_type: this.formType,
        signals,
      });
      await this._refreshDevices();
      this.formName = "";
      this.formOn = null;
      this.formOff = null;
      this.formTrigger = null;
      this.error = null;
    } catch (err) {
      this.error = err?.message || "Failed to create device";
    }
  }

  async _deleteDevice(deviceId) {
    await this.hass.callWS({ type: "raspyrfm/device/delete", device_id: deviceId });
    await this._refreshDevices();
  }

  async _handleStartLearning() {
    await this.hass.callWS({ type: "raspyrfm/learning/start" });
    this.learning = true;
  }

  async _handleStopLearning() {
    await this.hass.callWS({ type: "raspyrfm/learning/stop" });
    this.learning = false;
  }
}

customElements.define("raspyrfm-panel", RaspyRFMPanel);
