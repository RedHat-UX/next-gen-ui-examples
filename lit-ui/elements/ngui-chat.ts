import { LitElement, html } from 'lit';
import { customElement } from 'lit/decorators.js';

import { PfTextInput } from '@patternfly/elements/pf-text-input/pf-text-input.js';

@customElement('ngui-chat')
export class NguiChat extends LitElement {
  #chatUrl = 'http://localhost:8000/runs/'
  #sessionId = crypto.randomUUID();
  render() {
    return html`
      <form @submit="${this.#onSubmit}">
        <pf-text-input name="input"
                       value="tell me about toy story"
                       @keyup="${this.#onKeyup}"></pf-text-input>
      </form>
    `;
  }

  #onKeyup(event: KeyboardEvent) {
    if (event.key === 'Enter')
      (event.target as HTMLElement).closest('form')?.requestSubmit()
  }

  async #onSubmit(event: Event) {
    event.preventDefault();

    if (event.target instanceof HTMLFormElement) {
      const form = event.target
      const input = form.elements.namedItem('input') as PfTextInput;

      this.#sessionId ??= crypto.randomUUID();
      const response = await fetch(this.#chatUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({
          agent_name:"movies",
          session_id: this.#sessionId,
          session:{
            id: this.#sessionId,
            history:[], // todo: append history
            state: "bananas",
          },
          mode:"sync",
          input:[{
            role:"user",
            parts:[{
              name:"<string>",
              content: input.value,
            }],
          }],
        })
      })
        .then(response => response.json())
        .catch(err => console.error(err));

      console.log(response);
    }
  }
}
