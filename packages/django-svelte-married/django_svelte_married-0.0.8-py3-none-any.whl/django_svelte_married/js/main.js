import exported from './exported';

if (!window.__SVELTE) window.__SVELTE = {};

for (const [mountId, {component, props}] of Object.entries(window.SVELTE_RENDER)) {
    if (window.__SVELTE[mountId]) window.__SVELTE[mountId].$destroy();
    window.__SVELTE[mountId] = new exported[component]({
        target: document.getElementById(mountId),
        props,
        hydrate: true
    });
}
