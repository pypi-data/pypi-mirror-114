class Registry {
  constructor(registry = {}) {
    this._registry = registry;
  }

  getComponent = (tagName) => {
    return this._registry[tagName] || undefined;
  };

  register = (tagName, klass) => {
    this._registry[tagName] = klass;
    klass.prototype.tagName = tagName;
    klass.tagName = tagName;
  };
}

const registry = new Registry();
export { registry };
