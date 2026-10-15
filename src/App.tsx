import { FormEvent, useEffect, useMemo, useState } from "react";

type IconName =
  | "drop"
  | "lock"
  | "eye"
  | "chevron"
  | "waste"
  | "check"
  | "clock"
  | "route"
  | "bolt"
  | "cancel"
  | "box"
  | "play"
  | "filter"
  | "search"
  | "hospital"
  | "truck"
  | "alert"
  | "user"
  | "logout"
  | "refresh"
  | "sun"
  | "moon"
  | "expand";

const Icon = ({ name, size = 20 }: { name: IconName; size?: number }) => {
  const paths: Record<IconName, React.ReactNode> = {
    drop: <path d="M12 2.6S5.5 9.2 5.5 14.6a6.5 6.5 0 0 0 13 0C18.5 9.2 12 2.6 12 2.6Z" />,
    lock: <><rect x="5" y="10" width="14" height="11" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></>,
    eye: <><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" /><circle cx="12" cy="12" r="2.5" /></>,
    chevron: <path d="m9 18 6-6-6-6" />,
    waste: <><path d="M4 7h16M9 7V4h6v3m3 0-1 14H7L6 7" /><path d="M10 11v6m4-6v6" /></>,
    check: <path d="m5 12 4 4L19 6" />,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    route: <><circle cx="5" cy="6" r="2" /><circle cx="19" cy="18" r="2" /><path d="M7 6h4a3 3 0 0 1 3 3v6a3 3 0 0 0 3 3" /></>,
    bolt: <path d="m13 2-8 12h7l-1 8 8-12h-7l1-8Z" />,
    cancel: <><circle cx="12" cy="12" r="9" /><path d="m9 9 6 6m0-6-6 6" /></>,
    box: <><path d="m4 7 8-4 8 4-8 4-8-4Z" /><path d="m4 7 8 4 8-4v10l-8 4-8-4V7Zm8 4v10" /></>,
    play: <path d="m8 5 11 7-11 7V5Z" />,
    filter: <path d="M4 6h16M7 12h10m-7 6h4" />,
    search: <><circle cx="10.5" cy="10.5" r="6.5" /><path d="m16 16 4 4" /></>,
    hospital: <><path d="M4 21V6h16v15M8 21v-5h8v5M9 10h6m-3-3v6" /></>,
    truck: <><path d="M3 6h11v11H3V6Zm11 4h4l3 4v3h-7v-7Z" /><circle cx="7" cy="18" r="2" /><circle cx="18" cy="18" r="2" /></>,
    alert: <><path d="M12 3 2.5 20h19L12 3Z" /><path d="M12 9v5m0 3h.01" /></>,
    user: <><circle cx="12" cy="8" r="4" /><path d="M4 21a8 8 0 0 1 16 0" /></>,
    logout: <><path d="M10 4H5v16h5m4-4 4-4-4-4m4 4H9" /></>,
    refresh: <><path d="M20 7v5h-5" /><path d="M19 12a7 7 0 1 0-2 5" /></>,
    sun: <><circle cx="12" cy="12" r="4" /><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42" /></>,
    moon: <path d="M20.5 15.6A8.5 8.5 0 0 1 8.4 3.5 8.5 8.5 0 1 0 20.5 15.6Z" />,
    expand: <><path d="M8 3H3v5m13-5h5v5M8 21H3v-5m13 5h5v-5" /></>,
  };

  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {paths[name]}
    </svg>
  );
};

const Logo = ({ compact = false }: { compact?: boolean }) => (
  <div className="logo">
    <span className="logo-mark">
      <svg viewBox="0 0 38 44" aria-hidden="true">
        <path d="M19 1.5S3.5 17.2 3.5 29.5A15.5 15.5 0 0 0 34.5 29.5C34.5 17.2 19 1.5 19 1.5Z" fill="currentColor" />
        <path d="M19 18v15M11.5 25.5h15" stroke="white" strokeWidth="4" strokeLinecap="round" />
      </svg>
    </span>
    {!compact && <span>Blood<span>Stock</span></span>}
  </div>
);

const ThemeToggle = ({ dark, onToggle }: { dark: boolean; onToggle: () => void }) => (
  <button className="theme-toggle" onClick={onToggle} aria-label={`Switch to ${dark ? "light" : "dark"} theme`} title={`Switch to ${dark ? "light" : "dark"} theme`}>
    <span className={!dark ? "selected" : ""}><Icon name="sun" size={14} /></span>
    <span className={dark ? "selected" : ""}><Icon name="moon" size={14} /></span>
  </button>
);

function BloodIllustration() {
  return (
    <svg className="hero-art" viewBox="0 0 640 520" role="img" aria-label="Blood donation and healthcare illustration">
      <circle cx="340" cy="235" r="173" fill="#fff5f5" />
      <circle cx="349" cy="213" r="120" fill="#4A90C2" />
      <path d="M270 126c32-29 87-37 127-13l-16 25-35 1-17 22-35 5-30-17 6-23Zm-35 93 36-27 35 13 8 35-18 33-31-2-28-25-2-27Zm122 26 34-29 57 5-6 49-34 44-31-19-20-50Z" fill="#9CC8E3" />
      <path d="M405 106c40 20 68 61 68 108 0 67-54 121-121 121-35 0-66-15-88-39" fill="none" stroke="#286D9E" strokeWidth="7" strokeLinecap="round" />

      <g transform="translate(72 88) rotate(-8 80 120)">
        <path d="M55 21h52v24H55z" fill="#F9B6B3" />
        <path d="M64 0h34v23H64z" fill="#B3262E" />
        <rect x="30" y="42" width="102" height="158" rx="25" fill="white" stroke="#B3262E" strokeWidth="5" />
        <path d="M36 118c25-17 61 13 90-7v64a19 19 0 0 1-19 19H55a19 19 0 0 1-19-19v-57Z" fill="#EF6461" />
        <path d="M80 72v37M61.5 90.5h37" stroke="#B3262E" strokeWidth="8" strokeLinecap="round" />
        <path d="M81 200v45c0 17 20 19 20 36" fill="none" stroke="#B3262E" strokeWidth="5" strokeLinecap="round" />
      </g>

      <g transform="translate(414 286) rotate(9)">
        <rect x="5" y="0" width="42" height="135" rx="20" fill="#fff" stroke="#4A90C2" strokeWidth="5" />
        <path d="M9 68h34v46a17 17 0 0 1-34 0V68Z" fill="#EF6461" />
        <rect x="0" y="0" width="52" height="23" rx="8" fill="#286D9E" />
        <rect x="63" y="-13" width="42" height="135" rx="20" fill="#fff" stroke="#4A90C2" strokeWidth="5" />
        <path d="M67 59h34v42a17 17 0 0 1-34 0V59Z" fill="#F4A261" />
        <rect x="58" y="-13" width="52" height="23" rx="8" fill="#286D9E" />
      </g>

      <path d="M91 414c55-39 119-43 164-9 27 20 57 31 90 31h146v76H198c-36 0-71-13-98-36l-9-62Z" fill="#E8A27D" />
      <path d="M259 405c23-36 59-53 86-34 20 14 32 46 62 43l64-6 20 28H345c-33 0-62-10-86-31Z" fill="#F3B491" />
      <path d="M134 389v96h-52c-27 0-48-22-48-48s21-48 48-48h52Z" fill="#EF6461" />
      <rect x="126" y="389" width="70" height="96" rx="17" fill="#B3262E" />
      <path d="M161 417c-12-18-35 0-19 16l19 18 19-18c16-16-7-34-19-16Z" fill="white" />

      <path d="M511 100c18-31 35-32 44-6-27 16-44 38-55 67" fill="none" stroke="#B3262E" strokeWidth="8" strokeLinecap="round" />
      <path d="M510 130c14-24 38-27 53-15-13 21-33 29-53 15Zm-4-12c-2-27-18-40-38-39 0 24 14 40 38 39Z" fill="#EF6461" />
      <g fill="#B3262E">
        <path d="M560 199h8v31h-8zM548 211h32v8h-32z" />
        <path d="M84 47h7v27h-7zM74 57h27v7H74z" />
      </g>
      <path d="M550 343c0-16 19-26 31-14 12-12 31-2 31 14 0 16-31 37-31 37s-31-21-31-37Z" fill="#EF6461" />
    </svg>
  );
}

function Login({ onLogin, dark, onTheme }: { onLogin: () => void; dark: boolean; onTheme: () => void }) {
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    window.setTimeout(() => {
      setLoading(false);
      if (password.toLowerCase() === "wrong") setError("Incorrect password. Please try again.");
      else onLogin();
    }, 750);
  };

  return (
    <main className="login-page">
      <div className="login-theme"><ThemeToggle dark={dark} onToggle={onTheme} /></div>
      <section className="login-visual">
        <div className="visual-logo"><Logo /></div>
        <div className="plus plus-one">+</div>
        <div className="plus plus-two">+</div>
        <BloodIllustration />
        <div className="tagline">
          <span>Network-wide blood planning</span>
          <h1>Right blood. Right place.<br />Before it expires.</h1>
          <p>Smarter allocation for a healthier hospital network.</p>
        </div>
      </section>
      <section className="login-side">
        <div className="mobile-logo"><Logo /></div>
        <form className="login-card" onSubmit={submit}>
          <div className="eyebrow">SECURE STAFF PORTAL</div>
          <h2>Hospital Staff Login</h2>
          <p className="muted">Welcome back. Enter your credentials to continue.</p>
          {error && <div className="error-message"><Icon name="alert" size={18} /><span>{error}</span></div>}
          <label>
            Staff ID / Email
            <input type="email" placeholder="e.g. ananya@hospital.org" defaultValue="ananya@hospital.org" />
          </label>
          <label>
            Password
            <div className="input-wrap">
              <Icon name="lock" size={18} />
              <input type={showPassword ? "text" : "password"} placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} />
              <button type="button" className="icon-button" aria-label="Show password" onClick={() => setShowPassword(!showPassword)}><Icon name="eye" size={19} /></button>
            </div>
          </label>
          <label>
            Hospital
            <select defaultValue="sms"><option value="sms">Sawai Man Singh Hospital</option><option>Rukmani Care</option><option>Jaipur General</option></select>
          </label>
          <div className="form-row">
            <label className="checkbox"><input type="checkbox" defaultChecked /><span>Remember me</span></label>
            <button className="link" type="button">Forgot password?</button>
          </div>
          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? <><span className="spinner" /> Signing in...</> : <>Sign in <span>→</span></>}
          </button>
          <p className="security-note"><Icon name="lock" size={14} /> Protected hospital network access</p>
        </form>
        <p className="legal">Planning tool using synthetic data. Not for clinical decisions.</p>
      </section>
    </main>
  );
}

const hospitals = [
  { id: "sms", short: "SMS", name: "Sawai Man Singh", stock: 142, x: 48, y: 44 },
  { id: "ru", short: "RC", name: "Rukmani Care", stock: 67, x: 72, y: 26 },
  { id: "jg", short: "JG", name: "Jaipur General", stock: 89, x: 77, y: 66 },
  { id: "am", short: "AM", name: "Amber Medical", stock: 43, x: 30, y: 19 },
  { id: "mh", short: "MH", name: "Mansarovar Health", stock: 105, x: 24, y: 75 },
  { id: "eh", short: "EH", name: "Eastline Hospital", stock: 58, x: 91, y: 45 },
];

const recommendations = [
  { urgent: true, source: "Sawai Man Singh", dest: "Rukmani Care", type: "Platelets", group: "B+", status: "Feasible", eta: "24 min", reason: "Expires soonest among compatible units" },
  { urgent: true, source: "Jaipur General", dest: "Eastline Hospital", type: "Red cells", group: "O−", status: "Feasible", eta: "18 min", reason: "Critical request; shortest viable route" },
  { urgent: false, source: "Amber Medical", dest: "Sawai Man Singh", type: "Plasma", group: "AB+", status: "Feasible", eta: "31 min", reason: "Balances network safety stock" },
  { urgent: false, source: "Mansarovar Health", dest: "Jaipur General", type: "Red cells", group: "A+", status: "Blocked", eta: "—", reason: "Nearest unit expires 20 min before arrival" },
];

type BagStatus = "safe" | "warning" | "critical" | "expired";

function BloodBag({ id, group, component, seconds, hospital, reserved, compact = false }: { id: string; group: string; component: string; seconds: number; hospital: string; reserved?: string; compact?: boolean }) {
  const [remaining, setRemaining] = useState(seconds);
  useEffect(() => {
    const timer = window.setInterval(() => setRemaining((time) => Math.max(-1, time - 1)), 1000);
    return () => window.clearInterval(timer);
  }, []);
  const status: BagStatus = remaining < 0 ? "expired" : remaining < 7200 ? "critical" : remaining < 86400 ? "warning" : "safe";
  const fill = status === "expired" ? 0 : Math.max(8, Math.min(92, (remaining / (component === "Platelets" ? 432000 : 3024000)) * 100));
  const formatTime = () => {
    if (remaining < 0) return "Expired";
    const days = Math.floor(remaining / 86400);
    const hours = Math.floor((remaining % 86400) / 3600);
    if (days > 0) return `${days}d ${hours}h`;
    if (remaining >= 86400 / 4) return `${hours}h ${Math.floor((remaining % 3600) / 60)}m`;
    const h = String(hours).padStart(2, "0");
    const m = String(Math.floor((remaining % 3600) / 60)).padStart(2, "0");
    const s = String(remaining % 60).padStart(2, "0");
    return `${h}:${m}:${s}`;
  };
  const exact = useMemo(() => new Date(Date.now() + Math.max(remaining, 0) * 1000).toLocaleString([], { dateStyle: "medium", timeStyle: "short" }), []);
  return (
    <div className={`blood-bag ${status} ${compact ? "compact" : ""}`} tabIndex={0} data-tooltip={`${id} · ${hospital}\nExpires ${exact}${reserved ? `\nReserved for ${reserved}` : ""}`}>
      <div className="bag-hanger" />
      <div className="bag-shell">
        <div className="bag-fill" style={{ height: `${fill}%` }} />
        <span className="bag-cross">+</span>
        {status === "critical" && <span className="bag-warning"><Icon name="alert" size={10} /></span>}
      </div>
      <div className="bag-tube" />
      <b>{group}</b>
      <small>{component}</small>
      <time>{formatTime()}</time>
    </div>
  );
}

function MapPanel() {
  const [selected, setSelected] = useState(hospitals[0]);
  return (
    <section className="panel map-panel">
      <div className="panel-heading">
        <div><span className="section-kicker">LIVE NETWORK</span><h2>Jaipur hospital network</h2></div>
        <div className="map-legend"><span><i className="green-line" /> Feasible</span><span><i className="red-line" /> Blocked</span></div>
      </div>
      <div className="map">
        <div className="map-grid" />
        <span className="road road-1" /><span className="road road-2" /><span className="road road-3" /><span className="road road-4" />
        <span className="route route-1" /><span className="route route-2" /><span className="route route-3 blocked" /><span className="route route-4" />
        {hospitals.map((hospital) => (
          <button key={hospital.id} className={`marker marker-${hospital.id} ${selected.id === hospital.id ? "active" : ""}`} style={{ left: `${hospital.x}%`, top: `${hospital.y}%` }} onClick={() => setSelected(hospital)}>
            <span className="marker-icon"><Icon name="hospital" size={16} /></span>
            <span className="marker-label"><b>{hospital.short}</b><small>{hospital.stock} units</small></span>
          </button>
        ))}
        <div className="map-label label-one">JAIPUR</div>
        <div className="map-label label-two">TONK ROAD</div>
        <div className="hospital-popup">
          <button onClick={() => setSelected(hospitals[0])}>×</button>
          <div className="popup-top"><span className="mini-hospital"><Icon name="hospital" size={18} /></span><div><b>{selected.name}</b><small>Updated 2 min ago</small></div></div>
          <div className="popup-bags">
            <BloodBag compact id={`${selected.short}-041`} group="O−" component="RBC" seconds={196200} hospital={selected.name} />
            <BloodBag compact id={`${selected.short}-118`} group="B+" component="Platelets" seconds={5412} hospital={selected.name} reserved="Request #12" />
            <BloodBag compact id={`${selected.short}-209`} group="AB+" component="Plasma" seconds={72200} hospital={selected.name} />
          </div>
        </div>
      </div>
    </section>
  );
}

function ScenarioPanel() {
  const [notice, setNotice] = useState("");
  const [requests, setRequests] = useState(4);
  const applied = (message: string) => setNotice(message);
  return (
    <aside className="panel scenarios">
      <div className="panel-heading scenario-title"><div><span className="section-kicker">WHAT-IF PLANNING</span><h2>Scenario controls</h2></div><span className="live-dot">READY</span></div>
      {notice && <div className="scenario-notice"><Icon name="refresh" size={18} /><span>{notice}</span><button onClick={() => setNotice("")}>×</button></div>}
      <div className="scenario-card">
        <span className="scenario-icon coral"><Icon name="route" /></span>
        <div className="scenario-content"><b>Transport failure</b><small>Block a route temporarily</small><select><option>SMS → Rukmani Care</option><option>Jaipur General → Eastline</option></select></div>
        <button onClick={() => applied("Route SMS to Rukmani failed. 2 transfers replanned.")}>Apply</button>
      </div>
      <div className="scenario-card">
        <span className="scenario-icon amber-bg"><Icon name="bolt" /></span>
        <div className="scenario-content wide"><b>Demand spike</b><small>Urgent requests: <strong>{requests}</strong></small><input type="range" min="1" max="12" value={requests} onChange={(e) => setRequests(Number(e.target.value))} /></div>
      </div>
      <div className="scenario-card">
        <span className="scenario-icon blue-bg"><Icon name="cancel" /></span>
        <div className="scenario-content"><b>Cancellation</b><small>Remove a pending request</small><select><option>REQ-1842 · B+ platelets</option><option>REQ-1839 · O− red cells</option></select></div>
        <button onClick={() => applied("Request REQ-1842 cancelled. Stock released.")}>Apply</button>
      </div>
      <div className="scenario-card stock-arrival">
        <span className="scenario-icon green-bg"><Icon name="box" /></span>
        <div className="scenario-content wide">
          <b>New stock arrival</b><small>Add incoming inventory</small>
          <div className="mini-grid"><select><option>SMS Hospital</option><option>Jaipur General</option></select><select><option>Red cells</option><option>Platelets</option><option>Plasma</option></select><select><option>O+</option><option>A+</option><option>B−</option></select><input type="number" defaultValue="10" aria-label="Quantity" /></div>
        </div>
      </div>
      <button className="demo-button" onClick={() => applied("Demo applied. 5 urgent requests optimized across 3 hospitals.")}><Icon name="play" size={17} /> Run demo scenario</button>
    </aside>
  );
}

function Recommendations() {
  return (
    <div className="table-wrap">
      <div className="tab-tools">
        <div className="search"><Icon name="search" size={17} /><input placeholder="Search recommendations" /></div>
        <button className="tool-button"><Icon name="filter" size={17} /> All components</button>
        <button className="tool-button">Sort: Urgency <Icon name="chevron" size={15} /></button>
      </div>
      <div className="table-scroll">
        <table>
          <thead><tr><th>Source</th><th>Destination</th><th>Component & group</th><th>Feasibility</th><th>ETA</th><th>Reason</th><th /></tr></thead>
          <tbody>{recommendations.map((row, i) => (
            <tr key={i} className={row.status === "Blocked" ? "blocked-row" : ""}>
              <td><span className="hospital-cell"><i><Icon name="hospital" size={14} /></i><b>{row.source}</b></span></td>
              <td><b>{row.dest}</b></td>
              <td><span className="component"><Icon name="drop" size={16} /><span><b>{row.type}</b><small>{row.group}</small></span>{row.urgent && <em>Urgent</em>}</span></td>
              <td><span className={`status ${row.status.toLowerCase()}`}>{row.status === "Feasible" ? <Icon name="check" size={13} /> : <Icon name="cancel" size={13} />}{row.status}</span></td>
              <td><span className="eta"><Icon name="clock" size={15} />{row.eta}</span></td>
              <td className="reason">{row.reason}</td>
              <td><button className="row-action">→</button></td>
            </tr>
          ))}</tbody>
        </table>
      </div>
    </div>
  );
}

const inventoryHospitals = [
  { name: "Sawai Man Singh", short: "SMS", total: 142, units: [{ id: "SMS-041", c: "RBC", g: "O+", seconds: 374400 }, { id: "SMS-118", c: "Platelets", g: "B+", seconds: 4812, reserved: "Request #12" }, { id: "SMS-209", c: "Plasma", g: "AB+", seconds: 1555200 }] },
  { name: "Rukmani Care", short: "RC", total: 67, units: [{ id: "RC-052", c: "RBC", g: "A+", seconds: 108000 }, { id: "RC-122", c: "Platelets", g: "O+", seconds: 32940 }, { id: "RC-230", c: "Plasma", g: "B+", seconds: -1 }] },
  { name: "Jaipur General", short: "JG", total: 89, units: [{ id: "JG-034", c: "RBC", g: "O−", seconds: 205200 }, { id: "JG-105", c: "Platelets", g: "A+", seconds: 19200 }, { id: "JG-251", c: "Plasma", g: "A−", seconds: 6200 }] },
];

function Inventory() {
  const [sortSoonest, setSortSoonest] = useState(false);
  return (
    <div>
      <div className="tab-tools"><div className="search"><Icon name="search" size={17} /><input placeholder="Search hospital or blood group" /></div><button className="tool-button"><Icon name="filter" size={17} /> Blood group</button><button className={`tool-button ${sortSoonest ? "active" : ""}`} onClick={() => setSortSoonest(!sortSoonest)}>Sort by expiring soonest <Icon name="chevron" size={15} /></button></div>
      <div className="expiry-legend"><b>Expiry state</b><span><i className="safe" /> Safe</span><span><i className="warning" /> Expiring soon</span><span><i className="critical" /> Under 2 hours</span><span><i className="expired" /> Expired</span><small>Hover or focus a bag for unit details</small></div>
      <div className="inventory-grid">{inventoryHospitals.map((h) => (
        <article className="inventory-card" key={h.name}>
          <div className="inventory-head"><span className="mini-hospital"><Icon name="hospital" size={18} /></span><div><b>{h.name}</b><small>{h.total} units available</small></div><span className="healthy">Healthy</span></div>
          <div className="blood-bag-grid">{[...h.units].sort((a, b) => sortSoonest ? a.seconds - b.seconds : 0).map((u) => <BloodBag key={u.id} id={u.id} group={u.g} component={u.c} seconds={u.seconds} hospital={h.name} reserved={u.reserved} />)}</div>
        </article>
      ))}</div>
    </div>
  );
}

function Comparison() {
  const [split, setSplit] = useState(50);
  const [fullscreen, setFullscreen] = useState(false);
  const [replaying, setReplaying] = useState(false);
  const replay = () => {
    setReplaying(true);
    setSplit(8);
    window.setTimeout(() => setSplit(50), 250);
    window.setTimeout(() => setReplaying(false), 900);
  };
  return (
    <div className={`comparison-workspace ${fullscreen ? "fullscreen" : ""}`}>
      <div className="comparison-controls">
        <div><span className="section-kicker">DECISION REPLAY</span><h3>Before / after allocation</h3></div>
        <div className="comparison-actions"><select aria-label="Scenario"><option>Normal day</option><option>Transport failure</option><option>Demand spike</option></select><button onClick={replay}><Icon name="play" size={15} /> {replaying ? "Replaying..." : "Replay"}</button><button onClick={() => setFullscreen(!fullscreen)}><Icon name="expand" size={15} /> {fullscreen ? "Exit" : "Full screen"}</button></div>
      </div>
      <div className="split-stage">
        <div className="compare-side baseline-side">
          <div className="compare-title"><span>01</span><div><small>BASELINE PLAN</small><b>Nearest Available</b></div></div>
          <MiniPlan optimized={false} />
          <div className="assignments"><b>Assignments</b><span><i>1</i> SMS → Rukmani <em>O− RBC</em></span><span className="expired-assignment"><i>2</i> Mansarovar → General <em>Expired in transit</em></span><span><i>3</i> Amber → SMS <em>AB+ Plasma</em></span></div>
          <div className="compare-metrics"><span><small>Units wasted</small><b>8</b></span><span><small>Urgent served</small><b>9/12</b></span><span><small>Average ETA</small><b>42m</b></span></div>
        </div>
        <div className="compare-side optimizer-side" style={{ clipPath: `inset(0 0 0 ${split}%)` }}>
          <div className="compare-title"><span>02</span><div><small>RECOMMENDED PLAN</small><b>BloodStock Optimizer</b></div><em>WINNING PLAN</em></div>
          <MiniPlan optimized />
          <div className="assignments"><b>Assignments</b><span><i>1</i> Jaipur General → Eastline <em>O− RBC</em></span><span><i>2</i> SMS → Rukmani <em>B+ Platelets</em></span><span><i>3</i> Amber → SMS <em>AB+ Plasma</em></span></div>
          <div className="compare-metrics winning"><span><small>Units wasted</small><b>2</b><em>−6 units</em></span><span><small>Urgent served</small><b>12/12</b><em>+3 served</em></span><span><small>Average ETA</small><b>28m</b><em>−14 min</em></span></div>
        </div>
        <input className="split-slider" type="range" min="5" max="95" value={split} onChange={(event) => setSplit(Number(event.target.value))} aria-label="Reveal baseline or optimizer plan" />
        <div className="split-handle" style={{ left: `${split}%` }}><span>‹</span><span>›</span></div>
      </div>
      <div className="comparison-banner"><Icon name="bolt" size={17} /><b>Same scenario. Same data. Different decisions.</b><span>Drag the divider to inspect each allocation plan.</span></div>
    </div>
  );
}

function MiniPlan({ optimized }: { optimized: boolean }) {
  return (
    <div className={`mini-map ${optimized ? "optimized" : ""}`}>
      <span className="mini-road one" /><span className="mini-road two" /><span className="mini-route one" /><span className="mini-route two" /><span className={`mini-route three ${optimized ? "" : "failed"}`} />
      {[["SMS", 45, 46], ["RC", 72, 25], ["JG", 76, 68], ["AM", 25, 22], ["MH", 22, 75]].map(([name, x, y]) => <i key={name} style={{ left: `${x}%`, top: `${y}%` }}><Icon name="hospital" size={12} /><small>{name}</small></i>)}
      {!optimized && <span className="expired-unit"><Icon name="alert" size={12} /> 6 units expired</span>}
      {optimized && <span className="optimized-note"><Icon name="check" size={12} /> All urgent requests covered</span>}
    </div>
  );
}

function StyleGuide({ onClose }: { onClose: () => void }) {
  return (
    <div className="guide-backdrop" role="dialog" aria-modal="true" aria-label="BloodStock design system">
      <div className="style-guide">
        <div className="guide-head"><div><span className="section-kicker">BLOODSTOCK UI 1.0</span><h2>Component library & style guide</h2><p>Semantic tokens support both Light Ward and Control Room modes.</p></div><button onClick={onClose}>×</button></div>
        <section><h3>Color variables</h3><div className="swatches"><span className="swatch primary"><i /><b>Primary</b><small>Blood red</small></span><span className="swatch accent"><i /><b>Accent</b><small>Coral</small></span><span className="swatch info"><i /><b>Info</b><small>Medical blue</small></span><span className="swatch success"><i /><b>Success</b><small>Feasible</small></span><span className="swatch warning"><i /><b>Warning</b><small>Expiring</small></span><span className="swatch surface"><i /><b>Surface</b><small>Theme aware</small></span></div></section>
        <section><h3>Typography</h3><div className="type-samples"><div><span>Display / Inter Bold</span><b>Plan with confidence.</b></div><div><span>Body / Inter Regular</span><p>Clear, projector-ready operational information for every hospital.</p></div></div></section>
        <section><h3>Blood bag variants</h3><div className="guide-bags"><BloodBag id="VAR-001" group="O+" component="RBC" seconds={388800} hospital="Example Hospital" /><BloodBag id="VAR-002" group="A+" component="Platelets" seconds={20100} hospital="Example Hospital" /><BloodBag id="VAR-003" group="B−" component="RBC" seconds={5100} hospital="Example Hospital" /><BloodBag id="VAR-004" group="AB+" component="Plasma" seconds={-1} hospital="Example Hospital" /></div></section>
        <section><h3>Core controls</h3><div className="guide-controls"><button className="primary-button">Primary action</button><button className="outline-button">Secondary action</button><span className="status feasible"><Icon name="check" size={13} />Feasible</span><span className="status blocked"><Icon name="cancel" size={13} />Blocked</span></div></section>
        <section><h3>Operational states</h3><div className="state-grid"><div className="state-sample"><Icon name="drop" size={22} /><b>No matching units</b><small>Adjust filters to view more inventory.</small></div><div className="state-sample skeleton-state"><i /><i /><i /></div><div className="state-sample error-state"><Icon name="alert" size={22} /><b>Cannot reach server</b><small>Check the network and try again.</small><button><Icon name="refresh" size={13} /> Retry</button></div></div></section>
      </div>
    </div>
  );
}

function Dashboard({ onLogout, dark, onTheme }: { onLogout: () => void; dark: boolean; onTheme: () => void }) {
  const [plan, setPlan] = useState<"Optimizer" | "Baseline">("Optimizer");
  const [tab, setTab] = useState("Recommendations");
  const [menu, setMenu] = useState(false);
  const [guide, setGuide] = useState(false);
  const kpis = useMemo(() => plan === "Optimizer" ? [
    { label: "Units wasted", value: "24", change: "↓ 54 vs baseline", icon: "waste" as IconName, good: true },
    { label: "Requests fulfilled", value: "96%", change: "↑ 15% vs baseline", icon: "check" as IconName, good: true },
    { label: "Average ETA", value: "28 min", change: "↓ 14 min vs baseline", icon: "clock" as IconName, good: true },
  ] : [
    { label: "Units wasted", value: "78", change: "Current baseline", icon: "waste" as IconName, good: false },
    { label: "Requests fulfilled", value: "81%", change: "Current baseline", icon: "check" as IconName, good: false },
    { label: "Average ETA", value: "42 min", change: "Current baseline", icon: "clock" as IconName, good: false },
  ], [plan]);

  return (
    <main className="dashboard">
      <header className="topbar">
        <Logo />
        <div className="plan-toggle"><button className={plan === "Optimizer" ? "active" : ""} onClick={() => setPlan("Optimizer")}>Optimizer</button><button className={plan === "Baseline" ? "active" : ""} onClick={() => setPlan("Baseline")}>Baseline</button></div>
        <div className="topbar-right">
          <span className="synthetic-badge"><Icon name="alert" size={14} /> Synthetic data — not for clinical decisions</span>
          <button className="guide-button" onClick={() => setGuide(true)}>UI guide</button>
          <ThemeToggle dark={dark} onToggle={onTheme} />
          <div className="profile-wrap">
            <button className="profile" onClick={() => setMenu(!menu)}><span className="avatar">AM</span><span><b>Dr. Ananya Mehta</b><small>Sawai Man Singh Hospital</small></span><Icon name="chevron" size={16} /></button>
            {menu && <div className="profile-menu"><button><Icon name="user" size={17} /> Profile</button><button onClick={onLogout}><Icon name="logout" size={17} /> Logout</button></div>}
          </div>
        </div>
      </header>
      <div className="dashboard-body">
        <div className="welcome"><div><span className="section-kicker">TUESDAY, 18 JUNE</span><h1>Good morning, Ananya.</h1><p>Here’s how the Jaipur network is performing right now.</p></div><button className="outline-button"><Icon name="refresh" size={17} /> Refresh plan <small>Updated 2 min ago</small></button></div>
        <section className="kpi-grid">{kpis.map((kpi, i) => <article className="kpi" key={kpi.label}><span className={`kpi-icon kpi-${i}`}><Icon name={kpi.icon} /></span><div><span>{kpi.label}</span><strong>{kpi.value}</strong><small className={kpi.good ? "positive" : ""}>{kpi.change}</small></div><div className="sparkline"><i /><i /><i /><i /><i /><i /></div></article>)}</section>
        <div className="main-grid"><MapPanel /><ScenarioPanel /></div>
        <section className="panel tabs-panel">
          <div className="tabs-header"><div className="tabs">{["Recommendations", "Inventory", "Comparison"].map((item) => <button key={item} className={tab === item ? "active" : ""} onClick={() => setTab(item)}>{item}{item === "Recommendations" && <span>4</span>}</button>)}</div><span className="plan-label"><i /> Showing {plan.toLowerCase()} plan</span></div>
          {tab === "Recommendations" && <Recommendations />}
          {tab === "Inventory" && <Inventory />}
          {tab === "Comparison" && <Comparison />}
        </section>
      </div>
      {guide && <StyleGuide onClose={() => setGuide(false)} />}
    </main>
  );
}

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [dark, setDark] = useState(false);
  return <div className={dark ? "theme-dark" : "theme-light"}>{loggedIn ? <Dashboard dark={dark} onTheme={() => setDark(!dark)} onLogout={() => setLoggedIn(false)} /> : <Login dark={dark} onTheme={() => setDark(!dark)} onLogin={() => setLoggedIn(true)} />}</div>;
}
