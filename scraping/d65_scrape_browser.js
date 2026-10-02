// Browser version of d65_scrape.py, used for the 2026-10-01 pull.
// The dashboard (data.district65.net) wasn't reachable from the scripting environment's network, so the same
// Dash callbacks were run from the dashboard's own page in a browser. Paste into the dev-tools console on
// https://data.district65.net/, run `await D.run()`, then `D.download()` saves d65_dashboard_all_long.csv.
// Then: python3 scraping/build_from_long.py data/dashboard_YYYY-MM-DD   (writes the tidy CSVs)
// Checks: each school's IEP pie must equal its enrollment (rerun until it does); schools must sum to the district.
// Built with help from Claude (AI), which can make mistakes. Please verify.
window.D = {};
D.call = async function (outContains, inputs, state = [], changed = []) {
  D.deps = D.deps || await fetch('/_dash-dependencies').then(r => r.json());
  const cb = D.deps.find(d => d.output.includes(outContains) && !d.clientside_function);
  const spec = cb.output;
  const split = p => { const [id, prop] = p.split('@')[0].split('.'); return { id, property: prop }; };
  const outs = spec.startsWith('..') ? spec.slice(2, -2).split('...').map(split) : split(spec);
  const body = { output: spec, outputs: outs, inputs, state, changedPropIds: changed };
  for (let a = 0; a < 4; a++) {
    const r = await fetch('/_dash-update-component', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    if (r.status === 204) return {};
    if (r.ok) return (await r.json()).response;
    await new Promise(res => setTimeout(res, 2000 * (a + 1)));
  }
  throw new Error('call failed ' + outContains);
};
D.dec = function (v) {  // Plotly base64 typed arrays
  if (v && typeof v === 'object' && !Array.isArray(v) && 'bdata' in v) {
    const bin = atob(v.bdata), buf = new ArrayBuffer(bin.length), u8 = new Uint8Array(buf);
    for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    const m = { i1: Int8Array, u1: Uint8Array, i2: Int16Array, u2: Uint16Array, i4: Int32Array, u4: Uint32Array, f4: Float32Array, f8: Float64Array };
    return Array.from(new m[v.dtype.replace(/[<>|=]/, '')](buf));
  }
  return v;
};
D.strip = s => (s || '').replace(/<[^>]+>/g, '');
D.texts = node => { const out = []; const walk = x => { if (typeof x === 'string' || typeof x === 'number') out.push(String(x)); else if (Array.isArray(x)) x.forEach(walk); else if (x && typeof x === 'object') walk(x.children !== undefined ? x.children : (x.props || {}).children); }; walk(node); return out; };
D.bin10 = x => { x = +x; if (x >= 100) return '100+'; const b = Math.floor(x / 10) * 10; return `${b}-${b + 9}`; };
D.flatten = function (scope, page, resp, test = '') {  // same rules as flatten() in d65_scrape.py
  const rows = [];
  for (const [cid, v] of Object.entries(resp || {})) {
    const base = { scope, page, test_type: test, chart_id: cid };
    if (cid.startsWith('students-count')) {
      for (const t of D.texts(v.children)) { const m = t.match(/^(.*?):\s*([\d.]+)$/); if (m) rows.push({ ...base, chart_title: 'summary counts', series: '', category: m[1], value: +m[2] }); }
      continue;
    }
    const fig = v && typeof v === 'object' ? v.figure : null; if (!fig) continue;
    const title = D.strip(((fig.layout || {}).title || {}).text);
    for (const t of (fig.data || [])) {
      const typ = t.type, name = t.name || '';
      if (typ === 'box') continue;
      if (typ === 'indicator') { rows.push({ ...base, chart_title: title || D.strip((t.title || {}).text), series: '', category: 'value', value: t.value }); continue; }
      if (typ === 'histogram') {
        const c = {}; (D.dec(t.x) || []).forEach(x => { const k = D.bin10(x); c[k] = (c[k] || 0) + 1; });
        Object.keys(c).sort((a, b) => (a === '100+' ? 1000 : parseInt(a)) - (b === '100+' ? 1000 : parseInt(b)))
          .forEach(k => rows.push({ ...base, chart_title: `${title} (counts, 10-pt bins)`, series: name, category: k, value: c[k] }));
        continue;
      }
      const x = D.dec(t.x !== undefined ? t.x : t.labels) || [], y = D.dec(t.y !== undefined ? t.y : t.values) || [];
      const [cat, val] = t.orientation === 'h' ? [y, x] : [x, y];
      for (let i = 0; i < Math.min(cat.length, val.length); i++) rows.push({ ...base, chart_title: title, series: name, category: cat[i], value: val[i] });
    }
  }
  return rows;
};
D.TESTS = ['STAR Reading', 'STAR Early Literacy', 'STAR Reading Spanish', 'STAR Early Literacy Spanish', 'i-Ready Math'];
D.stores = ['bm-df', 'iready-df', 'star-df', 'star-el-df', 'star-es-df', 'star-el-es-df'];
D.run = async function () {
  D.init = await D.call('ps-df-current.data', [{ id: 'dummy', property: 'children' }]);
  const key = k => D.init[k].data;
  const filtered = async school => {
    const r = await D.call('ps-df-current-filter.data',
      [{ id: 'ps-df-current', property: 'data', value: key('ps-df-current') }, { id: 'apply-filters-btn', property: 'n_clicks', value: 1 }, { id: 'reset-filters-btn', property: 'n_clicks', value: null }],
      D.stores.map(s => ({ id: s, property: 'data', value: key(s) })).concat([
        { id: 'school-filter', property: 'value', value: school ? [school] : null }, { id: 'grade-filter', property: 'value', value: null },
        { id: 'race-filter', property: 'value', value: null }, { id: 'iep-filter', property: 'value', value: [] }, { id: 'el-filter', property: 'value', value: [] }, { id: 'lunch-filter', property: 'value', value: [] }]),
      ['apply-filters-btn.n_clicks']);
    const F = {}; for (const [k, v] of Object.entries(r)) if (v && typeof v === 'object' && 'data' in v) F[k.replace('-filter', '')] = v.data; return F;
  };
  const studentPages = async (label, school) => {
    const F = await filtered(school);
    const d = (i, k) => ({ id: i, property: 'data', value: F[k] }), url = p => ({ id: 'url', property: 'pathname', value: p });
    let rows = D.flatten(label, 'home', await D.call('home-grade.figure', [d('ps-df-current-filter', 'ps-df-current'), d('bm-df-filter', 'bm-df'), url('/')], [], ['url.pathname']));
    rows = rows.concat(D.flatten(label, 'attendance', await D.call('att-ada.figure', [d('ps-df-current-filter', 'ps-df-current'), url('/students/attendance')], [], ['url.pathname'])));
    rows = rows.concat(D.flatten(label, 'discipline', await D.call('lvl.figure', [d('bm-df-filter', 'bm-df'), url('/students/discipline')], [], ['url.pathname'])));
    for (const tt of D.TESTS) rows = rows.concat(D.flatten(label, 'assessments', await D.call('ast-graph-1.figure', [d('iready-df-filter', 'iready-df'), d('star-df-filter', 'star-df'), d('star-el-df-filter', 'star-el-df'), d('star-es-df-filter', 'star-es-df'), d('star-el-es-df-filter', 'star-el-es-df'), { id: 'test-type-dropdown', property: 'value', value: tt }, url('/students/assessments')], [], ['test-type-dropdown.value']), tt));
    return rows;
  };
  const consistent = rows => { const iep = rows.filter(r => r.chart_id === 'home-iep').reduce((a, r) => a + r.value, 0); const e = rows.find(r => r.chart_id === 'home-enrollment'); return e && iep === e.value; };
  D.rows = [];
  for (const school of [null].concat(D.init['school-filter'].options)) {
    let rows; for (let a = 0; a < 4; a++) { rows = await studentPages(school || 'District', school); if (consistent(rows)) break; await new Promise(r => setTimeout(r, 3000)); }
    D.rows = D.rows.concat(rows.map(r => ({ dataset: 'students', ...r })));
  }
  const per = new Set(['global-use-school', 'ghg-school', 'cost-savings-school']);
  for (const acct of ['All'].concat(D.init['accounts'].data)) {
    const r = await D.call('global-use.figure', [{ id: 'energyCAP-data', property: 'data', value: key('energyCAP-data') }, { id: 'ghg-df', property: 'data', value: key('ghg-df') }, { id: 'account-dropdown-menu', property: 'value', value: acct }, { id: 'url', property: 'pathname', value: '/sustainability/utility-usage' }], [], ['account-dropdown-menu.value']);
    D.rows = D.rows.concat(D.flatten(acct, 'utility-usage', r).filter(x => acct === 'All' || !per.has(x.chart_id)).map(x => ({ dataset: 'energy', ...x })));
  }
  return D.rows.length;
};
D.download = function () {
  const cols = ['dataset', 'scope', 'page', 'test_type', 'chart_id', 'chart_title', 'series', 'category', 'value'];
  const q = v => { if (v === null || v === undefined) return ''; const s = String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  const csv = cols.join(',') + '\n' + D.rows.map(r => cols.map(c => q(r[c])).join(',')).join('\n') + '\n';
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' })); a.download = 'd65_dashboard_all_long.csv'; a.click();
};
