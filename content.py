# -*- coding: utf-8 -*-
"""
Page bodies for the Auth Refactor docs. Helpers (code, diagram, table,
callout, h2/h3, verdict pills, cc) are injected by build.py via bind().
Keeping content here keeps build.py focused on the shell/templating.
"""

def bind(g):
    for name in ["esc", "code", "diagram", "callout", "h2", "h3",
                 "table", "CH", "RJ", "NE", "WN", "cc", "crumbs"]:
        globals()[name] = g[name]

def chip(text):
    return '<span class="chip">%s</span>' % text

def metabar(commit, files, add, dele, principle):
    return ('<div class="hero-meta">'
            + chip('Commit <code>%s</code>' % commit)
            + chip('%s files changed' % files)
            + chip('<span style="color:var(--good)">+%d</span>&nbsp;/&nbsp;<span style="color:var(--bad)">&minus;%d</span> lines' % (add, dele))
            + chip(principle)
            + '</div>')

# ======================================================================
# 00 — OVERVIEW
# ======================================================================
TITLE_00 = "Authentication Refactor — Jio_Leh Engineering Notes"
DESC_00 = ("A complete, in-depth record of the Jio_Leh authentication refactor: "
           "the problems, every option weighed, the decisions and the reasoning behind them.")

def body_00():
    b = []
    b.append('<div class="hero">')
    b.append('<span class="eyebrow">refactor/authentication &middot; 2026-06-16</span>')
    b.append('<h1>The Authentication Refactor, in full</h1>')
    b.append('<p class="lead">A self-contained record of the Jio_Leh auth refactor &mdash; '
             'not just <em>what</em> changed, but the full thinking process: the problems we found, '
             'every option we weighed (from the naïve approach to the preferred one), the trade-offs, '
             'the decision and its justification, the resulting code, and the tests.</p>')
    b.append(metabar("eb018f4 &rarr; c7b348f", "many", 706, 361, "Flutter + Supabase"))
    b.append('</div>')

    b.append('<div class="statgrid">'
             '<div class="statbox"><div class="n">6</div><div class="l">focused changes</div></div>'
             '<div class="statbox"><div class="n">20</div><div class="l">gate tests passing</div></div>'
             '<div class="statbox"><div class="n">0</div><div class="l">analyzer warnings</div></div>'
             '<div class="statbox"><div class="n">0</div><div class="l">user-facing changes</div></div>'
             '</div>')

    b.append(callout(
        "This site is written for <strong>future-us</strong>. Six months from now, when someone asks "
        "&ldquo;why is auth split into all these files?&rdquo;, this is the answer. Each change has its own page; "
        "read them in order &mdash; each one builds on the previous.", "info", "How to read this"))

    b.append(h2("what", "What this is"))
    b.append('<p>The auth feature already <em>worked</em>. A code review then surfaced five weaknesses plus a '
             'messy folder layout. <strong>None were user-visible bugs</strong> &mdash; every one was a '
             'maintainability, testability, or correctness risk. We fixed them as six small, ordered commits, '
             'each one the smallest change that fully solves its problem (no over-engineering for a student-sized app).</p>')

    b.append(h2("starting-point", "The starting point — what was wrong"))
    b.append(table(
        ["#", "Weakness", "What was wrong", "Fixed in"],
        [
            ["1", "<strong>Tangled test hooks</strong>",
             "<code>AuthService</code> took five nullable function parameters that existed only so tests could fake behaviour, and every method branched " + cc("if (hook != null)") + " between a fake path and a real path.",
             '<a href="01-auth-service-interface.html">01</a>'],
            ["2", "<strong>Inconsistent injection</strong>",
             "Only <code>AuthGate</code> accepted injected services; the login and onboarding screens grabbed the global <code>Services</code> singleton directly, so they were impossible to unit-test.",
             '<a href="02-service-provider-di.html">02</a>'],
            ["3", "<strong>One widget, three jobs</strong>",
             "<code>AuthGate</code> decided the screen, buffered deep links, and rendered &mdash; trapping genuinely tricky logic (&ldquo;hold a profile link until ready&rdquo;) inside a widget where it could not be unit-tested.",
             '<a href="03-auth-gate-split.html">03</a>'],
            ["4", "<strong>Race condition</strong>",
             "The gate&rsquo;s async resolve could be triggered several times concurrently; a slower, older check could finish last and overwrite a newer correct result. It could also crash by notifying after disposal.",
             '<a href="04-race-condition-fix.html">04</a>'],
            ["5", "<strong>Swallowed errors</strong>",
             "Auth failures were caught and discarded with no logging, and surfaced as a single generic &ldquo;Unexpected Error&rdquo; &mdash; undiagnosable and unhelpful.",
             '<a href="05-error-logging.html">05</a>'],
            ["&mdash;", "<strong>Half-organized tree</strong>",
             "Some features had folders, some didn&rsquo;t; auth-gate logic lived under <code>routing/</code>; a widget lived under <code>services/</code>.",
             '<a href="06-directory-reorganization.html">06</a>'],
        ]))

    b.append(h2("method", "The method we followed (identical for every change)"))
    b.append('<ol>'
             '<li><strong>Elaborate the problem</strong> in plain language, grounded in the real code.</li>'
             '<li><strong>Ladder the options</strong> from &ldquo;naïve&rdquo; (Level 0) to &ldquo;smart&rdquo; (Level 3&ndash;4), each with pros, cons, and trade-offs.</li>'
             '<li><strong>Decide</strong> &mdash; pick the smallest change that fully solves it, without over-engineering for a student-sized project.</li>'
             '<li><strong>Implement, prove with tests, then run</strong> <code>flutter analyze</code>.</li>'
             '</ol>')
    b.append(callout(
        "Stop climbing the ladder the moment the problem is solved. Going further (DI frameworks, full "
        "repository layers, stream-cancellation operators) was real, but over-engineered for this app&rsquo;s size.",
        "bulb", "Recurring rule of thumb:"))

    b.append(h2("principles", "The SWE principles used (glossary)"))
    b.append('<div class="glossary">'
             + _g("Dependency Inversion", "DIP", "Depend on an abstraction you own, not on a concrete vendor library.", "01, 02")
             + _g("Dependency Injection", "DI", "Be handed your dependencies from outside instead of fetching globals yourself.", "02")
             + _g("Single Responsibility", "SRP", "A class should have one reason to change.", "03")
             + _g("Logic / UI separation", "", "Pure Dart classes are easy to test; widgets should stay thin.", "03, 04")
             + _g("Concurrency correctness", "", "When async tasks overlap, the newest result must win &mdash; not the slowest.", "04")
             + _g("Observability", "", "Log the real cause so failures in the wild can be diagnosed.", "05")
             + _g("Cohesion by feature", "", "Group files by the feature they serve; keep folders single-purpose.", "06")
             + '</div>')

    b.append(h2("commits", "Commits, in order"))
    b.append('<div class="timeline">'
             + _tl("eb018f4", "refactor: split AuthService into interface + Supabase implementation", 6, 150, 204)
             + _tl("aff250d", "refactor: inject services via ServiceProvider instead of global", 5, 118, 26)
             + _tl("8d4ebdd", "refactor: split AuthGate into model + link holder + thin widget", 6, 326, 105)
             + _tl("6a6dbc7", "refactor: AuthGateModel to handle stale checks (race fix)", 2, 53, 1)
             + _tl("d8dcf32", "refactor: error logging for authentication processes", 2, 9, 5)
             + _tl("c7b348f", "refactor: restructure dir tree", 21, 50, 20)
             + '</div>')

    b.append(h2("changes", "The six changes"))
    b.append('<div class="cards">'
             + _card("01", "auth-service-interface", "AuthService Interface",
                     "Testability via abstraction &mdash; depend on an interface you own, not on Supabase.", 150, 204, 6)
             + _card("02", "service-provider-di", "ServiceProvider DI",
                     "Be handed your dependencies, instead of reaching for the global cupboard.", 118, 26, 5)
             + _card("03", "auth-gate-split", "AuthGate Split",
                     "One widget doing three jobs becomes a model + a link holder + a thin widget.", 326, 105, 6)
             + _card("04", "race-condition-fix", "Race Condition Fix",
                     "The newest async result must win &mdash; and never notify after disposal.", 53, 1, 2)
             + _card("05", "error-logging", "Error Logging & Honest Messages",
                     "Stop swallowing the cause; log it, and say something true to the user.", 9, 5, 2)
             + _card("06", "directory-reorganization", "Directory Reorganization",
                     "Organize by feature; keep every folder cohesive and single-purpose.", 50, 20, 21)
             + '</div>')

    b.append(h2("layout", "Final folder layout"))
    b.append(code(r'''
lib/
├─ app/
│  ├─ app.dart
│  └─ service_provider.dart      (DI wiring — an InheritedWidget)
├─ pages/
│  ├─ auth/
│  │  ├─ gate/
│  │  │  ├─ auth_gate.dart            (thin widget: listens + renders + navigates)
│  │  │  ├─ auth_gate_model.dart      (ChangeNotifier: decides the screen)
│  │  │  ├─ auth_gate_resolver.dart   (pure: maps state → result)
│  │  │  ├─ deep_link_parser.dart     (pure: parses profile links)
│  │  │  └─ profile_link_holder.dart  (pure: hold link until ready)
│  │  ├─ login_page.dart / login_widgets.dart
│  │  └─ onboarding_page.dart / onboarding_widgets.dart
│  ├─ map/
│  ├─ profile/   (profile_page, profile_edit_page, share_code_page)
│  └─ friends/   (friends_page)
├─ routing/
│  └─ app_routing.dart            (navigation only)
├─ services/
│  ├─ auth_service.dart           (interface + exceptions)
│  ├─ supabase_auth_service.dart  (real impl — the only auth file touching Supabase)
│  └─ account_service.dart, pin_service.dart, friends_service.dart,
│     location_service.dart, geocoding_service.dart, services.dart
├─ models/ · config/ · theme.dart
test/  mirrors lib/  (notably test/pages/auth/gate/ and test/services/fakes/)
''', name="lib/ — after the refactor", lang="text"))

    b.append(h2("result", "Result"))
    b.append('<ul>'
             '<li>All auth logic that matters is now unit-tested <strong>without spinning up Flutter or Supabase</strong>: '
             'the <code>AuthService</code> adapter (via mocktail), and <code>AuthGateModel</code>, '
             '<code>ProfileLinkHolder</code>, <code>deep_link_parser</code>, and <code>auth_gate_resolver</code> as pure/headless tests.</li>'
             '<li><code>flutter analyze</code> is clean across <code>lib</code> + <code>test</code>; <strong>20 gate tests pass</strong>.</li>'
             '<li>The app&rsquo;s behaviour for the user is <strong>unchanged</strong>; the internals are now testable, diagnosable, consistent, and organized.</li>'
             '</ul>')
    b.append(callout('Start with <a href="01-auth-service-interface.html"><strong>Change 01 — AuthService Interface</strong></a>. '
                     'Each page ends with a link to the next.', "good", "Next:"))
    return "".join(b)

def _g(title, word, desc, where):
    w = ' <span class="gw">%s</span>' % word if word else ""
    return ('<div class="gcard"><div class="gt">%s%s</div>'
            '<div class="gd">%s <span class="muted">&rarr; %s</span></div></div>'
            % (title, w, desc, where))

def _tl(h, msg, files, add, dele):
    return ('<div class="tl-item"><span class="dot"></span>'
            '<div class="tl-hash">%s</div>'
            '<div class="tl-msg">%s</div>'
            '<div class="tl-stat">%d files &middot; <span class="add">+%d</span> <span class="del">&minus;%d</span></div>'
            '</div>' % (h, msg, files, add, dele))

def _card(num, slug, title, desc, add, dele, files):
    return ('<a class="card" href="%s-%s.html">'
            '<div class="cnum">CHANGE %s</div>'
            '<div class="ctitle">%s</div>'
            '<div class="cdesc">%s</div>'
            '<div class="cstat"><span class="add">+%d</span><span class="del">&minus;%d</span><span>%d files</span></div>'
            '</a>' % (num, slug, num, title, desc, add, dele, files))

# ======================================================================
# 01 — AuthService Interface
# ======================================================================
TITLE_01 = "01 — AuthService Interface · Jio_Leh Auth Refactor"
DESC_01 = "Testability via abstraction — the Dependency Inversion Principle."

def body_01():
    b = [crumbs("01 · AuthService Interface")]
    b.append('<span class="eyebrow">Change 01 &middot; Dependency Inversion</span>')
    b.append('<h1>AuthService Interface</h1>')
    b.append('<p class="lead">Testability via abstraction &mdash; the Dependency Inversion Principle.</p>')
    b.append(metabar("eb018f4", 6, 150, 204, "Dependency Inversion (DIP)"))

    b.append(h2("problem", "1. The problem"))
    b.append('<p><code>AuthService</code>&rsquo;s constructor took five optional functions that existed '
             '<em>only</em> so tests could fake behaviour:</p>')
    b.append(code(r'''
AuthService({
  SupabaseClient? client,
  Session? Function()? currentSession,
  User? Function()? currentUser,
  Future<UserResponse> Function()? getUser,
  Future<void> Function()? signOut,
});''', name="auth_service.dart — before"))
    b.append('<p>Consequently every method had to branch on &ldquo;am I in a test?&rdquo;:</p>')
    b.append(code(r'''
User? getCurrentUser() {
  if (_currentUser != null) return _currentUser();   // fake path
  return _supabase.auth.currentUser;                 // real path
}'''))
    b.append('<p>The class mixed two unrelated concerns: (1) <strong>what it does</strong> (its real job) and '
             '(2) <strong>how we swap it out for tests</strong> (a construction concern). That produced four concrete pains.</p>')
    b.append(table(
        ["#", "Pain", "Explanation"],
        [
            ["1", "<strong>Smear</strong>", "The fake-vs-real check was scattered across every method, interleaving test wiring with production logic."],
            ["2", "<strong>Half-real objects</strong>", "You could inject a fake <code>currentSession</code> but leave the real <code>getUser</code> &mdash; so <code>isSignedIn()</code> is fake while <code>hasValidSession()</code> secretly hits the network. The type system <em>allowed</em> this broken mix."],
            ["3", "<strong>Invisible contract</strong>", "Asked &ldquo;what can <code>AuthService</code> do?&rdquo;, the constructor answered with plumbing (&ldquo;a client and four optional functions&rdquo;), not capabilities."],
            ["4", "<strong>Doesn&rsquo;t scale</strong>", "Adding one testable method = four edits in three places: the method, a constructor parameter, a field, and an <code>if</code>-branch."],
        ]))
    b.append(callout("one class doing both its job <em>and</em> its own test-swapping.", "warn", "Root cause:"))

    b.append(h2("options", "2. Options we discussed (naïve → preferred)"))
    b.append(table(
        ["Level", "Approach", "Pros", "Cons", "Verdict"],
        [
            ["0", "No seam &mdash; call Supabase directly", "Simplest code", "Untestable &mdash; <code>Supabase.instance</code> is a global needing real init", RJ()],
            ["1", "Function hooks (the original)", "Tests run without live Supabase", "All four pains above", RJ("Replaced")],
            ["2", "Inject the Supabase auth client (<code>GoTrueClient</code>)", "One injection point; no <code>if</code>-branches", "Still coupled to Supabase&rsquo;s type; tests mock Supabase&rsquo;s API; vendor lock-in", NE("Improvement only")],
            ["3", "<strong>Program to an interface you own</strong>", "No smear; no half-real objects; self-documenting; scales; DIP", "One extra file; interface still names Supabase types (<code>User</code>/<code>Session</code>)", CH()],
            ["4", "Full repository layer / codegen mocks", "Maximum flexibility", "Over-engineering for one service", RJ("Not chosen")],
        ]))
    b.append('<p><strong>Why Level 3 maps cleanly onto the four pains:</strong></p>')
    b.append('<ul>'
             '<li><strong>No smear</strong> &rarr; real logic lives only in <code>SupabaseAuthService</code>; fakes live only in <code>FakeAuthService</code>.</li>'
             '<li><strong>No half-real objects</strong> &rarr; an object is wholly real or wholly fake; you cannot mix.</li>'
             '<li><strong>Visible contract</strong> &rarr; the abstract class <em>is</em> the documentation.</li>'
             '<li><strong>Scales</strong> &rarr; a new capability is one interface method + two implementations.</li>'
             '</ul>')
    b.append(callout("This is the <strong>Dependency Inversion Principle</strong> &mdash; the app depends on an abstraction "
                     "it owns, not on Supabase. Swapping providers later means writing one new class and changing "
                     "<em>zero</em> tests.", "bulb", "Bonus:"))

    b.append(h2("placement", "3. File-placement decision"))
    b.append('<p><strong>Q:</strong> should the interface and implementation go in separate folders (<code>domain/</code> vs <code>data/</code>)?</p>')
    b.append('<p><strong>A:</strong> No &mdash; keep them side by side in <code>services/</code> for now. Separate folders pay off at a '
             'scale we are not at (many services, multiple impls each, a big team). The boundary is already enforced by two things '
             'we have: (1) the type everyone uses (<code>AuthService</code>, never the concrete class) and (2) one wiring point '
             '(<code>services.dart</code>).</p>')
    b.append(callout("the interface keeps the original filename <code>auth_service.dart</code>, so every existing "
                     "<code>import '.../auth_service.dart'</code> still resolves to the type &mdash; <strong>no consumer code changed</strong>. "
                     "Only two places ever construct an <code>AuthService</code>: <code>services.dart</code> and the unit test.",
                     "info", "Key trick:"))

    b.append(h2("changeset", "4. The change set (with code)"))
    b.append(h3("cs-interface", "auth_service.dart — now the interface + exceptions"))
    b.append(code(r'''
abstract class AuthService {
  // Primitives — each implementation provides these.
  User? getCurrentUser();
  bool isSignedIn();
  Future<bool> hasValidSession();
  Stream<AuthState> authStateChanges();
  Future<void> signInWithGoogle();
  Future<void> signOut();

  // Derived helpers — shared by all impls, written once.
  String? getCurrentUserEmail() => getCurrentUser()?.email;
  String getCurrentUserId() {
    final id = getCurrentUser()?.id;
    if (id == null) throw const NotSignedInException();
    return id;
  }
}''', name="lib/services/auth_service.dart"))
    b.append(h3("cs-impl", "supabase_auth_service.dart — the real impl"))
    b.append('<p>The only auth file that imports Supabase.</p>')
    b.append(code(r'''
class SupabaseAuthService extends AuthService {
  SupabaseAuthService({SupabaseClient? client}) : _client = client;
  final SupabaseClient? _client;
  SupabaseClient get _supabase => _client ?? Supabase.instance.client;

  @override bool isSignedIn() => _supabase.auth.currentSession != null;

  @override
  Future<bool> hasValidSession() async {
    if (!isSignedIn()) return false;
    try {
      final response = await _supabase.auth.getUser();
      return response.user != null;
    } on AuthException {
      return false;   // expired / deleted
    }
  }
  // ...getCurrentUser, authStateChanges, signInWithGoogle, signOut...
}''', name="lib/services/supabase_auth_service.dart"))
    b.append(h3("cs-services", "services.dart — the single place the app commits to Supabase"))
    b.append(code(r'''static final AuthService auth = SupabaseAuthService(client: _client);''',
                  name="lib/services/services.dart"))
    b.append('<p>Other services already declared their field as <code>AuthService</code>, so they needed no change. '
             'Using <code>extends AuthService</code> (not <code>implements</code>) lets both impls inherit the derived helpers for free.</p>')

    b.append(h2("testfork", "5. The test fork — a real decision"))
    b.append('<p>The old test relied on the deleted hooks. Its behaviours (e.g. &ldquo;<code>hasValidSession</code> returns false when '
             '<code>getUser</code> throws <code>AuthException</code>&rdquo;) are now real-adapter logic inside <code>SupabaseAuthService</code>. '
             'Two honest options:</p>')
    b.append(table(
        ["Option", "Pros", "Cons"],
        [
            ["<strong>A</strong> &mdash; Drop the micro-tests; rely on a fake in consumer tests", "No new dependency; fewer lines; common for thin adapters", "Loses direct coverage of the <code>AuthException</code>&rarr;false path"],
            ["<strong>B</strong> &mdash; Keep coverage with mocktail (mock <code>SupabaseClient</code> + <code>GoTrueClient</code>)", "Keeps exact coverage", "One dev dependency; mock-heavy tests"],
        ]))
    b.append(callout("Option <strong>B</strong> (chosen by the team).", "good", "Decision:"))
    b.append(code(r'''
class _MockSupabaseClient extends Mock implements SupabaseClient {}
class _MockGoTrueClient extends Mock implements GoTrueClient {}

when(() => client.auth).thenReturn(gotrue);
when(() => gotrue.currentSession).thenReturn(_session);
when(() => gotrue.getUser()).thenThrow(const AuthException('expired'));
await expectLater(auth.hasValidSession(), completion(isFalse));''',
                  name="test/services/auth_service_test.dart"))
    b.append('<p>The old <code>signOut</code> assertions were dropped because an earlier refactor already removed that '
             'side-effect from <code>hasValidSession</code>.</p>')

    b.append(h2("diagram", "6. Before / after"))
    b.append(diagram(r'''
BEFORE — one class, two tangled brains:

   +------------------------------------------+
   |               AuthService                |
   | - _client + 4 fake-hook functions        |
   | every method: if(hook!=null) fake : real |
   +------------------------------------------+
        | real                  | fake
        v                       v
   [ Supabase ]           [ test hooks ]''', "before"))
    b.append(diagram(r'''
AFTER — contract + two implementations:

                +-------------------------------+
                |  <<abstract>>  AuthService    |
                +-------------------------------+
                      ^                   ^
             extends  |                   | extends
        +----------------------+   +----------------------+
        | SupabaseAuthService  |   |   FakeAuthService    |
        +----------------------+   +----------------------+
                  |                          |
                  v                          v
             [ Supabase ]               [ tests ]

   services.dart picks the real one, once.
   Everyone else depends only on the contract.''', "after"))

    b.append(h2("result", "7. Result & what it unblocks"))
    b.append('<ul>'
             '<li><code>flutter analyze</code> clean; auth-service + resolver tests pass.</li>'
             '<li>No consumer code changed; the app names Supabase in exactly <strong>one line</strong>.</li>'
             '<li><strong>Unblocked Change 02:</strong> with an interface + a ready fake, injecting a fake into the login/onboarding screens becomes trivial.</li>'
             '</ul>')
    b.append(callout("<code>FakeAuthService</code> was added, then removed under <strong>YAGNI</strong> (Change 01&rsquo;s tests use "
                     "mocktail, not the fake), then re-added in Changes 03/04 when a real consumer test finally needed it. "
                     "The ladder works in both directions.", "info", "Note:"))
    return "".join(b)

# ======================================================================
# 02 — ServiceProvider DI
# ======================================================================
TITLE_02 = "02 — ServiceProvider Dependency Injection · Jio_Leh"
DESC_02 = "Consistent injection; stop reaching for globals."

def body_02():
    b = [crumbs("02 · ServiceProvider DI")]
    b.append('<span class="eyebrow">Change 02 &middot; Dependency Injection</span>')
    b.append('<h1>Dependency Injection via ServiceProvider</h1>')
    b.append('<p class="lead">Consistent injection; stop reaching for globals.</p>')
    b.append(metabar("aff250d", 5, 118, 26, "Dependency Injection (DI)"))

    b.append(h2("concept", "1. The core concept: how a class gets its dependencies"))
    b.append('<p>A <strong>dependency</strong> is anything a piece of code needs from outside itself. '
             '<code>AuthPage</code>&rsquo;s job is to draw the login screen, but to sign someone in it needs the auth service '
             '&mdash; so <code>AuthService</code> is a dependency of <code>AuthPage</code>. There are two fundamentally different '
             'ways to get a dependency, and the difference <em>is</em> this whole change.</p>')
    b.append(table(
        ['Way A — &ldquo;grab it yourself&rdquo;', 'Way B — &ldquo;be handed it&rdquo;'],
        [[cc("final _auth = Services.auth;") + "<br><span class='muted'>reaches into the global cupboard</span>",
          cc("const AuthGate({AuthService? auth, ...});") + "<br><span class='muted'>accepts what it needs</span>"]]))
    b.append(callout("&ldquo;Being handed your dependencies instead of grabbing them&rdquo; <strong>is</strong> Dependency Injection. "
                     "<code>AuthGate</code> used DI; <code>AuthPage</code> and <code>OnboardingPage</code> did not.", "quote", ""))

    b.append(h2("why-hurts", "2. Why “grabbing” hurts — the concrete failure"))
    b.append('<p>To test &ldquo;tapping Sign In calls <code>signInWithGoogle</code>&rdquo;, we must slip in a fake. But '
             '<code>AuthPage</code> has no <strong>door</strong> to receive one &mdash; it always runs <code>Services.auth</code>. '
             'And touching <code>Services.auth</code> is toxic in a test:</p>')
    b.append(code(r'''
class Services {
  static final _client = Supabase.instance.client;          // needs Supabase.initialize()
  static final AuthService auth = SupabaseAuthService(client: _client);
}''', name="lib/services/services.dart"))
    b.append('<p>The instant any code reads <code>Services.auth</code>, Dart builds <code>Supabase.instance.client</code>, and '
             '<code>Supabase.instance</code> <strong>throws</strong> unless <code>Supabase.initialize()</code> already ran &mdash; '
             'which only happens in <code>main()</code> against the real backend. So:</p>')
    b.append('<ol>'
             '<li><code>AuthPage</code> grabs <code>Services.auth</code> itself (no door to pass a fake).</li>'
             '<li><code>Services.auth</code> builds a real Supabase-backed service.</li>'
             '<li>Real Supabase needs a live, initialized connection.</li>'
             '<li>&rarr; You cannot test <code>AuthPage</code> at all without standing up real infrastructure. This is <strong>tight coupling</strong>.</li>'
             '</ol>')
    b.append(h3("seam", "The “seam” idea"))
    b.append('<p>A <strong>seam</strong> is a place where you can change behaviour without editing the code &mdash; like a seam in '
             'fabric where two pieces can be separated. <code>AuthGate</code>&rsquo;s constructor parameter was a seam (a test slips in '
             'a fake there). <code>AuthPage</code> had none. Change 01 created the seam at the <em>type</em> level (interface + fake); '
             'Change 02 opens the <em>door</em> on each screen so the seam can be used.</p>')

    b.append(h2("options", "3. Options we discussed (naïve → preferred)"))
    b.append(table(
        ["Level", "Approach", "Pros", "Cons", "Verdict"],
        [
            ["0", "Leave it", "No work", "Screens untestable; inconsistent", NE("The problem")],
            ["1", "Make the global swappable (<code>Services.auth = Fake()</code>)", "No constructor change", "<span class='cons'>Shared mutable global state</span> &mdash; one test&rsquo;s fake leaks into the next; order-dependent failures", RJ("Anti-pattern")],
            ["2", "Constructor injection (optional param + fallback, like AuthGate)", "Consistent; no new dep; isolated per-test fakes; zero behaviour change", "Prop drilling in deep trees (not an issue here)", NE("Solid")],
            ["3", "<strong>InheritedWidget / Provider</strong> (ambient injection)", "No prop drilling; scales to deep trees; idiomatic; per-subtree overrides", "A concept to learn + the lifecycle gotcha", CH() + " ServiceProvider"],
            ["4", "DI framework (get_it, Riverpod)", "Powerful for big apps", "New dependency + mental model; overkill", RJ("Not chosen")],
        ]))
    b.append(callout("We deliberated Level 2 vs 3 at length. Level 2 was the smaller change; Level 3 was chosen so the student "
                     "could learn the pattern that underlies Provider/Riverpod/Bloc, and to future-proof a deepening widget tree.",
                     "info", "Deliberation:"))

    b.append(h2("inherited", "4. How InheritedWidget actually works (the depth)"))
    b.append('<ul>'
             '<li>It&rsquo;s a &ldquo;noticeboard&rdquo; mounted near the top of the tree; descendants read it via <code>ServiceProvider.of(context)</code>.</li>'
             '<li>That lookup is <strong>O(1)</strong>: every Element keeps a hash map of the InheritedWidgets above it, so <code>.of(context)</code> is a map lookup, <em>not</em> a tree walk.</li>'
             '<li><code>.of(context)</code> also <strong>subscribes</strong> the caller as a dependent; if the inherited data changes (governed by <code>updateShouldNotify</code>), only the dependents rebuild. Our services never change, so <code>updateShouldNotify</code> returns <code>false</code> &mdash; a pure lookup.</li>'
             '<li>Underlying patterns: <strong>Inversion of Control</strong> (the scope decides what you get), <strong>Ambient Context</strong>, <strong>hierarchical/scoped injection</strong>, and the <strong>Observer</strong> pattern. Provider/Riverpod/Bloc are all built on this primitive.</li>'
             '<li>A Service Locator (<code>Services.x</code>) <em>hides</em> dependencies; DI via context makes them explicit and overridable per subtree.</li>'
             '</ul>')

    b.append(h2("design", "5. Design decisions"))
    b.append(h3("d-name", "(a) Name"))
    b.append('<p>We chose <strong>ServiceProvider</strong> (file <code>service_provider.dart</code>) because &ldquo;Provider&rdquo; is the '
             'real beginner-standard term &mdash; Flutter&rsquo;s own tutorials use it &mdash; so it is friendly <em>and</em> '
             'industry-correct. Considered and rejected: ServiceShelf, AppServices, ServicesContext.</p>')
    b.append(h3("d-holds", "(b) What it holds — all services, with a lazy fallback"))
    b.append('<p>It exposes <strong>all</strong> services (not just auth+account). Each is an optional override that falls back '
             'lazily to the <code>Services</code> singletons:</p>')
    b.append(code(r'''AuthService get auth => _auth ?? Services.auth;''', name="lib/app/service_provider.dart"))
    b.append('<p>Three wins at once:</p>')
    b.append('<ul>'
             '<li><strong>Production</strong> mounts it with <em>no</em> arguments &rarr; everything real &rarr; zero behaviour change.</li>'
             '<li><strong>Tests</strong> override only what they use.</li>'
             '<li>Unused services are <strong>never instantiated</strong> (the fallback is lazy) &rarr; no Supabase in tests.</li>'
             '<li>You never edit the scope again when converting a new screen.</li>'
             '</ul>')
    b.append(h3("d-lifecycle", "(c) The lifecycle gotcha (important)"))
    b.append('<p>You <strong>cannot</strong> read <code>ServiceProvider.of(context)</code> in <code>initState</code> &mdash; the widget '
             'isn&rsquo;t wired into the tree yet, so <code>context</code> can&rsquo;t look upward. The correct place is '
             '<code>didChangeDependencies</code>, which runs right after <code>initState</code> and <em>does</em> have valid access '
             'to inherited widgets.</p>')
    b.append(table(
        ["Lifecycle method", "When", "Inherited widgets readable?"],
        [
            ["constructor", "object created", "<span class='cons'>no</span>"],
            ["<code>initState()</code>", "once, first setup", "<span class='cons'>no</span>"],
            ["<code>didChangeDependencies()</code>", "after initState, <em>and again</em> on dependency changes", "<span class='pros'>yes</span>"],
            ["<code>build()</code>", "many times", "<span class='pros'>yes</span>"],
        ]))
    b.append('<p>But <code>didChangeDependencies</code> can run <strong>more than once</strong> (a theme switch, screen rotation, or '
             'keyboard appearing all change inherited <code>Theme</code>/<code>MediaQuery</code>). One-time setup must therefore be '
             'guarded with a run-once boolean:</p>')
    b.append(code(r'''
bool _didInit = false;
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  if (_didInit) return;          // run-once guard
  _didInit = true;
  final services = ServiceProvider.of(context)!;
  _auth = services.auth;
  // ... one-time setup (subscribe, build model) ...
}'''))
    b.append(callout("re-running would re-subscribe to a stream (duplicate listeners + a memory leak) and re-assign "
                     "<code>late final</code> fields (a crash). <code>build()</code> is the &ldquo;runs many times&rdquo; method; "
                     "subscriptions, controllers, and final-assignments are &ldquo;set up once&rdquo;.", "warn", "Why once:"))

    b.append(h2("changeset", "6. The change set"))
    b.append(table(
        ["File", "Change"],
        [
            ["<code>service_provider.dart</code> <span class='muted'>(new; later moved to app/ in Change 06)</span>", "The InheritedWidget with all-service getters + lazy fallback."],
            ["<code>app.dart</code>", "Wrap <code>MaterialApp</code> in <code>ServiceProvider</code> (no overrides)."],
            ["<code>login_page.dart</code>", "Read <code>ServiceProvider.of(context)!.auth</code> in the button handler (easy case &mdash; runs after build)."],
            ["<code>onboarding_page.dart</code>", "Move service reads + display-name prefill from <code>initState</code> to <code>didChangeDependencies</code> (run-once)."],
            ["<code>auth_gate.dart</code>", "Drop the constructor&rsquo;s auth/account params; read services in <code>didChangeDependencies</code>; keep the context-free deep-link setup in <code>initState</code>."],
        ]))
    b.append('<p>Tests inject by wrapping with a scope holding fakes:</p>')
    b.append(code(r'''
ServiceProvider(
  auth: FakeAuthService(signedIn: true),  // override only what this test needs
  child: const MaterialApp(home: AuthPage()),
)'''))

    b.append(h2("diagram", "7. Diagrams"))
    b.append(diagram(r'''
PROP DRILLING (pure constructor injection, deep tree):
   App --auth--> Home --auth--> ProfileTab --auth--> Settings --auth--> Button
   (middle widgets relay something they never use)''', "the problem DI avoids"))
    b.append(diagram(r'''
ServiceProvider (ambient):
   [ServiceProvider at top] ...........................
       |                                               :
       App -> Home -> ProfileTab -> Settings -> Button --of(context) O(1)--> up
   (descendants reach UP; middle widgets untouched)''', "ambient injection"))

    b.append(h2("result", "8. Result"))
    b.append('<ul>'
             '<li><code>flutter analyze</code> clean. App behaviour unchanged (production uses the real services via fallback).</li>'
             '<li>All auth screens are now injectable the <strong>same</strong> way &mdash; consistency restored.</li>'
             '<li>The <code>FakeAuthService</code> from Change 01 finally has a real purpose here.</li>'
             '</ul>')
    return "".join(b)

# ======================================================================
# 03 — AuthGate Split
# ======================================================================
TITLE_03 = "03 — AuthGate Split · Jio_Leh Auth Refactor"
DESC_03 = "One widget, three jobs → model + link holder + thin widget (SRP)."

def body_03():
    b = [crumbs("03 · AuthGate Split")]
    b.append('<span class="eyebrow">Change 03 &middot; Single Responsibility</span>')
    b.append('<h1>Split AuthGate — model + link holder + thin widget</h1>')
    b.append('<p class="lead">One widget doing three jobs becomes three pieces, each with one reason to change.</p>')
    b.append(metabar("8d4ebdd", 6, 326, 105, "Single Responsibility (SRP)"))

    b.append(h2("problem", "1. The problem"))
    b.append('<p>A <strong>responsibility</strong> is one reason a class might change. The Single Responsibility Principle says a '
             'class should have only one. The test: finish the sentence &ldquo;this class is responsible for ____&rdquo; &mdash; if you '
             'need an &ldquo;and&rdquo;, that&rsquo;s a smell. <code>AuthGate</code> needed three:</p>')
    b.append(table(
        ["Job", "What", "Code involved"],
        [
            ["<strong>A</strong>", "Deep-link handling &mdash; hold a profile id until ready, then open it", "<code>_pendingProfileId</code>, <code>_handleLink</code>, <code>_openPendingProfile</code>"],
            ["<strong>B</strong>", "Auth state &mdash; decide login / onboarding / map / error", "<code>_state</code>, <code>_resolve</code>, the auth-change subscription"],
            ["<strong>C</strong>", "Rendering &mdash; turn state into widgets", "<code>build()</code>"],
        ]))
    b.append(h3("why-hurts", "Why mixing them hurts"))
    b.append('<ul>'
             '<li><strong>The hardest logic was trapped in a widget.</strong> Job A&rsquo;s rule &mdash; &ldquo;a link can arrive '
             '<em>before</em> the app is ready; hold it, then open once ready, exactly once&rdquo; &mdash; is stateful and '
             'timing-sensitive, but lived inside a <code>StatefulWidget</code>. Testing it needed full Flutter UI, a faked '
             '<code>app_links</code> stream, and pumped frames.</li>'
             '<li><strong>Changing one job risked breaking another</strong> &mdash; they shared <code>_state</code>, <code>context</code>, and fields.</li>'
             '<li><strong>Too much to read at a glance</strong> &mdash; a newcomer wanting &ldquo;the thing that picks the first screen&rdquo; '
             'also waded through deep-link buffering and navigation timing.</li>'
             '</ul>')
    b.append(callout("the scenario &ldquo;a link arrives while loading &rarr; must NOT navigate yet &rarr; once ready, open it exactly "
                     "once&rdquo; is a few lines of pure logic, but testing it required a heavy, brittle widget test.", "warn", "The concrete pain:"))

    b.append(h2("insight", "2. The key insight before the options"))
    b.append(callout("The three jobs are <strong>not equal</strong>. Rendering is inherently a widget; auth-state is orchestration; "
                     "deep-link buffering is <em>pure logic</em> with no reason to touch Flutter. So the goal is to get A and B "
                     "<strong>out</strong> of the widget, leaving C thin. &ldquo;Three files&rdquo; is the wrong axis &mdash; splitting "
                     "by <strong>kind of thing</strong> is the right one. (You can have three files and still be stuck if all three are widgets.)",
                     "bulb", "Insight:"))

    b.append(h2("options", "3. Options we discussed (naïve → preferred)"))
    b.append(table(
        ["Level", "Approach", "Pros", "Cons", "Verdict"],
        [
            ["0", "Leave it", "&mdash;", "Tricky logic stays untestable", NE("The problem")],
            ["1", "Split into three <em>widgets</em> (the literal &ldquo;three files&rdquo; idea)", "Shorter file; looks tidy", "<span class='cons'>Cosmetic</span> &mdash; link logic still inside a widget; still needs UI to test", RJ("Trap")],
            ["2", "<strong>Extract the pure logic, keep one thin widget</strong>", "Un-testable logic becomes trivially testable; widget shrinks; each piece changes for one reason", "Introduces the <code>ChangeNotifier</code> concept", CH()],
            ["3", "Also abstract the deep-link <em>source</em> (a <code>DeepLinkService</code>)", "Even the link&rarr;nav wiring testable headlessly", "More files/abstraction; over-engineered for a 1-link app", NE("Pocket for later")],
            ["4", "State-management library (Bloc/Riverpod)", "Powerful", "Overkill for one gate", RJ("Not chosen")],
        ]))
    b.append(callout("Level 2, doing <code>ProfileLinkHolder</code> first (smallest change, biggest testability win), then "
                     "<code>AuthGateModel</code>.", "good", "Decision:"))

    b.append(h2("naming", "4. Naming — kept beginner-friendly on purpose"))
    b.append('<p>The student asked for simple, non-enterprise names. We compared three &ldquo;themes&rdquo; and chose <strong>Theme A</strong>:</p>')
    b.append(table(
        ["Role", "Theme A (chosen)", "Theme B", "Theme C"],
        [
            ["Holds the link", "<strong>ProfileLinkHolder</strong>", "ProfileLinkBox", "SavedProfileLink"],
            ["Decides the screen", "<strong>AuthGateModel</strong>", "StartScreenPicker", "AuthGateBrain"],
            ["The enum", "<strong>AuthGateScreen</strong>", "StartScreen", "GateScreen"],
        ]))
    b.append('<p><strong>Why Theme A wins:</strong> <code>...Model</code> is the <em>actual</em> beginner-standard &mdash; Flutter&rsquo;s '
             'own Provider tutorial names <code>ChangeNotifier</code> classes like <code>CartModel</code>. So it&rsquo;s familiar, not '
             'jargon. We avoided &ldquo;controller&rdquo;, &ldquo;coordinator&rdquo;, &ldquo;resolver&rdquo;, &ldquo;pending&rdquo;, '
             '&ldquo;orchestration&rdquo;. (The pre-existing <code>auth_gate_resolver.dart</code> kept its name.) Enum values are named '
             'after the <strong>screen shown</strong> (<code>loading, login, onboarding, map, error</code>) so the code reads like English.</p>')
    b.append(callout("the student preferred <code>if/else</code> returns in <code>build()</code>. Trade-off recorded: a <code>switch</code> "
                     "on the enum gives <em>exhaustiveness checking</em> (the compiler warns if a new screen value is unhandled); "
                     "<code>if/else</code> loses that safety net &mdash; a forgotten new case would silently fall through to the error screen.",
                     "info", "if/else vs switch:"))

    b.append(h2("pieces", "5. The three pieces (skeletons)"))
    b.append(h3("p-holder", "ProfileLinkHolder — pure Dart, the big testability win"))
    b.append(code(r'''
class ProfileLinkHolder {
  String? _savedId;

  String? handleLink(Uri uri, {required bool isReady}) {
    final id = profileIdFromDeepLink(uri);
    if (id == null) return null;   // not a profile link
    if (isReady) return id;        // ready → open now
    _savedId = id;                 // else save for later
    return null;
  }

  String? takeSavedLink() { final id = _savedId; _savedId = null; return id; }
}''', name="lib/pages/auth/gate/profile_link_holder.dart"))
    b.append(h3("p-model", "AuthGateModel — a ChangeNotifier (not a widget), headless-testable"))
    b.append(code(r'''
enum AuthGateScreen { loading, login, onboarding, map, error }

class AuthGateModel extends ChangeNotifier {
  AuthGateModel({required this.auth, required this.account});
  AuthGateScreen _screen = AuthGateScreen.loading;
  AuthGateScreen get screen => _screen;
  StreamSubscription? _authChanges;

  void start() {
    _authChanges = auth.authStateChanges().listen((_) => check());
    check();
  }
  Future<void> check() async {
    _setScreen(AuthGateScreen.loading);
    try {
      final result = await resolveAuthGateState(...);
      _setScreen(switch (result) {
        AuthGateResult.signedOut       => AuthGateScreen.login,
        AuthGateResult.needsOnboarding => AuthGateScreen.onboarding,
        AuthGateResult.ready           => AuthGateScreen.map,
      });
    } catch (_) { _setScreen(AuthGateScreen.error); }
  }
  void _setScreen(AuthGateScreen s) { _screen = s; notifyListeners(); }
}''', name="lib/pages/auth/gate/auth_gate_model.dart"))
    b.append(h3("p-widget", "AuthGate widget — thin: wires the two, renders, navigates"))
    b.append(code(r'''
void _onModelChange() {
  setState(() {});
  if (_model.screen == AuthGateScreen.map) {
    final id = _linkHolder.takeSavedLink();
    if (id != null) _openProfile(id);
  }
}
void _onLink(Uri uri) {
  final id = _linkHolder.handleLink(uri, isReady: _model.screen == AuthGateScreen.map);
  if (id != null) _openProfile(id);
}''', name="lib/pages/auth/gate/auth_gate.dart"))
    b.append('<p>The widget still owns (correctly) the <code>AppLinks</code> subscription, the <code>Navigator.push</code>, and '
             'drawing &mdash; all inherently UI.</p>')

    b.append(h2("tests", "6. Tests — the payoff"))
    b.append('<ul>'
             '<li><code>profile_link_holder_test.dart</code> (4 tests): the hold-until-ready rule, e.g. &ldquo;<em>saves when not ready, then releases the id once</em>&rdquo;.</li>'
             '<li><code>auth_gate_model_test.dart</code> (6 tests): the full state machine (loading / login / onboarding / map / error), using <code>FakeAuthService</code> + a mocktail <code>MockAccountService</code>.</li>'
             '</ul>')
    b.append(callout("The scenario that used to need a full widget test is now a 3-line unit test. All passed; "
                     "<code>flutter analyze</code> clean.", "good", "Payoff:"))

    b.append(h2("diagram", "7. Diagram"))
    b.append(diagram(r'''
BEFORE: [AuthGate widget] = decide state + buffer link + render (all tangled)

AFTER:
   [AuthGateModel]            [ProfileLinkHolder]
   (ChangeNotifier, headless) (pure Dart)
        ^                          ^
        | listens                  | uses
        +----- [AuthGate widget: thin] -----+
                 (renders + navigates)''', "before → after"))

    b.append(h2("result", "8. Result"))
    b.append('<ul>'
             '<li>Three jobs, three pieces; the tricky logic is now pure and tested.</li>'
             '<li><code>AuthGate</code> reads like English (&ldquo;if screen == map, open the saved link&rdquo;).</li>'
             '<li><strong>Set up Change 04:</strong> the race guard now belongs in one place &mdash; <code>AuthGateModel.check()</code>.</li>'
             '</ul>')
    return "".join(b)

# ======================================================================
# 04 — Race Condition Fix
# ======================================================================
TITLE_04 = "04 — Race Condition Fix · Jio_Leh Auth Refactor"
DESC_04 = "The newest async result must win — and don't notify after disposal."

def body_04():
    b = [crumbs("04 · Race Condition Fix")]
    b.append('<span class="eyebrow">Change 04 &middot; Concurrency correctness</span>')
    b.append('<h1>Race Condition Fix in AuthGateModel.check()</h1>')
    b.append('<p class="lead">The newest async result must win &mdash; and don&rsquo;t notify after disposal.</p>')
    b.append(metabar("6a6dbc7", 2, 53, 1, "Concurrency correctness"))

    b.append(h2("problem", "1. The problem"))
    b.append('<p><code>check()</code> is <code>async</code>:</p>')
    b.append(code(r'''
Future<void> check() async {
  _setScreen(loading);
  final result = await resolveAuthGateState(...);   // takes time (network)
  _setScreen(...);                                   // runs LATER
}'''))
    b.append('<p>A <strong>race condition</strong> is when two things run at overlapping times and the final result depends on which '
             'finishes <em>last</em> &mdash; which you don&rsquo;t control. The enabler is <code>await</code>: while <code>check()</code> '
             'waits on the network, a <em>second</em> <code>check()</code> can start. And <code>check()</code> fires from several places '
             'that can land close together:</p>')
    b.append('<ul>'
             '<li><code>start()</code> at launch,</li>'
             '<li>every auth-state change (<code>authStateChanges().listen((_) =&gt; check())</code>),</li>'
             '<li>onboarding completion (<code>onComplete: _model.check</code>),</li>'
             '<li>the Retry button.</li>'
             '</ul>')
    b.append(h3("bug1", "Bug #1 — stale overwrite"))
    b.append(diagram(r'''
A: setScreen(loading); await ...(slow)
B: setScreen(loading); await ...(fast) → ready → setScreen(MAP)   ✅ newest, correct
A: ...returns signedOut (stale) → setScreen(LOGIN)                ❌ overwrites!''', "the bug"))
    b.append('<p>The user lands on the login screen although they are logged in, because the <em>older, slower</em> call A finished '
             'last and stamped its stale answer over B&rsquo;s correct one. Nothing told A &ldquo;you&rsquo;re out of date.&rdquo;</p>')
    b.append(h3("bug2", "Bug #2 — finishing after disposal"))
    b.append('<p>If <code>check()</code> is mid-<code>await</code> and the model is disposed (the widget is removed), the await '
             'completes and runs <code>_setScreen(...)</code> &rarr; <code>notifyListeners()</code> on a disposed '
             '<code>ChangeNotifier</code>:</p>')
    b.append(code(r'''A ChangeNotifier was used after being disposed.   → crash''', lang="text"))
    b.append('<p>The old widget guarded this with <code>if (!mounted) return</code>; the new model had no such guard (dropped when '
             'we moved logic out of the widget).</p>')
    b.append(callout("Both bugs are the same root issue: <strong>an async task finishing when its result is no longer wanted</strong> "
                     "&mdash; either superseded by a newer task, or the owner is gone.", "warn", "Root issue:"))

    b.append(h2("options", "2. Options we discussed (naïve → preferred)"))
    b.append(table(
        ["Level", "Approach", "Pros", "Cons", "Verdict"],
        [
            ["0", "Leave it", "&mdash;", "Occasional wrong screen + possible crash", NE("The problem")],
            ["1", "&ldquo;Busy&rdquo; flag &mdash; ignore new checks while one runs", "Tiny", "<span class='cons'>Actively wrong</span> &mdash; blocks the NEWEST call (freshest info) and lets the old one stamp a stale result. Makes the race worse.", RJ("Harmful")],
            ["2", "Disposed guard only", "Fixes the crash (#2)", "Does nothing for #1", NE("Half a fix")],
            ["3", "<strong>Request token + disposed guard</strong>", "Fixes both in ~4 lines; no dependency; encodes &ldquo;newest wins&rdquo;; testable", "Must remember the guard after every await (one path here)", CH()],
            ["4", "Real cancellation (<code>CancelableOperation</code>) / stream <code>switchMap</code>", "Also cancels wasted in-flight work", "New dependency/concept; overkill &mdash; the token gives the correct result without it", RJ("Not chosen")],
        ]))

    b.append(h2("fix", "3. The chosen fix (Level 3)"))
    b.append(code(r'''
int _latestCheck = 0;
bool _disposed = false;

Future<void> check() async {
  final myCheck = ++_latestCheck;            // claim the newest ticket
  _setScreen(AuthGateScreen.loading);
  try {
    final result = await resolveAuthGateState(...);
    if (_disposed || myCheck != _latestCheck) return;   // superseded or gone → drop
    _setScreen(...);
  } catch (error, stackTrace) {
    debugPrint('AuthGate check failed: $error\n$stackTrace');
    if (_disposed || myCheck != _latestCheck) return;
    _setScreen(AuthGateScreen.error);
  }
}

@override
void dispose() { _disposed = true; _authChanges?.cancel(); super.dispose(); }''',
                  name="lib/pages/auth/gate/auth_gate_model.dart"))
    b.append('<p>Every <code>check()</code> takes the next ticket number. When it finishes, it writes its result only if it still '
             'holds the <em>latest</em> ticket. A newer check that started after it supersedes it; the stale one drops its result.</p>')

    b.append(h2("trace", "4. Trace — the fix in action"))
    b.append(diagram(r'''
A: myCheck=1, latest=1, loading, await...
B: myCheck=2, latest=2, loading, await...
B done: 2 == latest(2) → setScreen(MAP)   ✅
A done: 1 != latest(2) → DROP              ✅ (no stale overwrite)
+ disposed guard → no crash if the model was thrown away mid-await.''', "newest wins"))

    b.append(h2("tests", "5. Tests"))
    b.append('<p>Added to <code>auth_gate_model_test.dart</code>, using <code>Completer</code>s so the test controls exactly when '
             'each <code>check()</code> finishes:</p>')
    b.append(code(r'''
final completers = <Completer<bool>>[];
when(() => account.profileExists()).thenAnswer((_) {
  final c = Completer<bool>(); completers.add(c); return c.future;
});

final older = model.check();
final newer = model.check();
await pumpEventQueue();          // both now waiting at profileExists()

completers[1].complete(true);    // finish the NEWER first → map
await pumpEventQueue();
expect(model.screen, AuthGateScreen.map);

completers[0].complete(false);   // finish the OLDER (stale) → would be onboarding
await pumpEventQueue();
expect(model.screen, AuthGateScreen.map);   // unchanged → stale dropped ✅''',
                  name="test/pages/auth/gate/auth_gate_model_test.dart"))
    b.append('<p>All model tests pass; <code>flutter analyze</code> clean.</p>')

    b.append(h2("result", "6. Result"))
    b.append('<ul>'
             '<li>The newest check always wins; a slow older check can&rsquo;t flip the screen back.</li>'
             '<li>A check finishing after dispose no longer crashes.</li>'
             '<li>Because Change 03 had centralized the logic, this fix lived in <strong>one place</strong> &mdash; '
             '<code>AuthGateModel.check()</code> &mdash; instead of being scattered in the widget.</li>'
             '</ul>')
    return "".join(b)

# ======================================================================
# 05 — Error Logging
# ======================================================================
TITLE_05 = "05 — Error Logging & Honest Messages · Jio_Leh"
DESC_05 = "Observability — stop swallowing the cause."

def body_05():
    b = [crumbs("05 · Error Logging")]
    b.append('<span class="eyebrow">Change 05 &middot; Observability</span>')
    b.append('<h1>Error Logging &amp; Honest Messages</h1>')
    b.append('<p class="lead">Observability &mdash; stop swallowing the cause.</p>')
    b.append(metabar("d8dcf32", 2, 9, 5, "Observability"))

    b.append(h2("problem", "1. The problem"))
    b.append('<p>Two auth failure points threw away information.</p>')
    b.append(h3("spot1", "Spot 1 — AuthPage._signInWithGoogle"))
    b.append(code(r'''
} catch (error) {
  _showSnackBar('Unexpected Error.');   // same message for everything;
}                                        // real cause discarded'''))
    b.append(h3("spot2", "Spot 2 — AuthGateModel.check"))
    b.append(code(r'''
} catch (_) {                            // cause not even named
  _setScreen(error);
}'''))
    b.append('<p>&ldquo;Swallowing an error&rdquo; = catching it and recording it nowhere. The program keeps running, but the '
             '<strong>evidence</strong> of what went wrong is destroyed.</p>')
    b.append(h3("facetA", "Facet A — you can't debug what you can't see (observability)"))
    b.append('<p>A user says &ldquo;I can&rsquo;t log in, it just says Unexpected Error.&rdquo; Why did it fail? A network timeout? A '
             'rejected OAuth? A bad redirect URL? A Supabase error? With no log, you have <strong>nothing</strong> &mdash; the one '
             'object that knew (the <code>error</code>) was discarded at the <code>catch</code>.</p>')
    b.append(h3("facetB", "Facet B — one message can't fit two situations"))
    b.append(table(
        ["Kind", "Example", "What the user should hear"],
        [
            ["Transient", "Wi-Fi blip, server briefly busy", "&ldquo;Network problem &mdash; try again.&rdquo;"],
            ["Real auth failure", "Sign-in rejected, account issue", "&ldquo;Sign-in failed.&rdquo; (retry won&rsquo;t help)"],
        ]))
    b.append('<p>Both produced the same scary, uninformative &ldquo;Unexpected Error.&rdquo; The code <em>had</em> the info (the '
             'error type) but discarded it before deciding what to say.</p>')
    b.append(callout("catching <em>everything</em> and reacting identically conflates explainable errors, retryable errors, and "
                     "genuine bugs &mdash; and a swallowed bug can hide for months.", "warn", "Smell:"))

    b.append(h2("decided", "2. What we decided (and a subtlety that simplified Facet B)"))
    b.append('<p>Fix applied:</p>')
    b.append('<ul>'
             '<li><strong>Always log</strong> the real cause + stack trace (Facet A &mdash; the most important).</li>'
             '<li>Give an <strong>honest, actionable</strong> message instead of &ldquo;Unexpected Error&rdquo;.</li>'
             '</ul>')
    b.append(callout("on mobile, <code>signInWithGoogle</code> <em>throwing here</em> means the OAuth flow could not <em>start</em> "
                     "(a launch/connectivity issue). An actual Google <em>rejection</em> does not throw here &mdash; it arrives later "
                     "via the auth stream. So a connection-oriented message (&ldquo;check your connection and try again&rdquo;) is the "
                     "<strong>correct</strong> one, and we did <em>not</em> need a transient-vs-auth type split in the UI. We "
                     "deliberately did not over-build this.", "info", "Subtlety on Facet B:"))
    b.append('<p><strong>Why <code>debugPrint</code>:</strong> simplest, idiomatic Flutter logging, fine for a student project; can '
             'be swapped for a logger / <code>dart:developer log</code> later.</p>')

    b.append(h2("changeset", "3. The change set"))
    b.append(h3("cs-login", "login_page.dart"))
    b.append(code(r'''
} catch (error, stackTrace) {
  debugPrint('Google sign-in failed: $error\n$stackTrace');
  if (mounted) {
    _showSnackBar('Could not start sign-in. Check your connection and try again.');
  }
}''', name="lib/pages/auth/login_page.dart"))
    b.append(h3("cs-model", "auth_gate_model.dart"))
    b.append(code(r'''
} catch (error, stackTrace) {
  debugPrint('AuthGate check failed: $error\n$stackTrace');
  if (_disposed || myCheck != _latestCheck) return;
  _setScreen(AuthGateScreen.error);
}''', name="lib/pages/auth/gate/auth_gate_model.dart"))
    b.append('<p>Logging happens <em>before</em> the stale/disposed guard, so even a dropped check&rsquo;s error is recorded.</p>')

    b.append(h2("diagram", "4. Before / after"))
    b.append(diagram(r'''
BEFORE: error → catch → [cause discarded] + "Unexpected Error" (always)
AFTER : error → catch → log(cause + stack) → honest, actionable message''', "before → after"))

    b.append(h2("result", "5. Result"))
    b.append('<ul>'
             '<li>Failures are now logged with a stack trace &rarr; a &ldquo;login broken&rdquo; report is diagnosable.</li>'
             '<li>The login message is honest about the real situation (couldn&rsquo;t <em>start</em> the flow = connectivity) instead '
             'of an uninformative &ldquo;Unexpected Error&rdquo;.</li>'
             '<li>The error-screen unit test now also exercises the logging path (the &ldquo;network down&rdquo; line in test output is '
             'the <code>debugPrint</code> working as intended).</li>'
             '</ul>')
    return "".join(b)

# ======================================================================
# 06 — Directory Reorganization
# ======================================================================
TITLE_06 = "06 — Directory Reorganization · Jio_Leh Auth Refactor"
DESC_06 = "Organize by feature; keep folders cohesive."

def body_06():
    b = [crumbs("06 · Directory Reorganization")]
    b.append('<span class="eyebrow">Change 06 &middot; Cohesion by feature</span>')
    b.append('<h1>Directory Reorganization</h1>')
    b.append('<p class="lead">Organize by feature; keep folders cohesive.</p>')
    b.append(metabar("c7b348f", 21, 50, 20, "Cohesion by feature"))

    b.append(h2("found", "1. The inconsistencies found"))
    b.append(table(
        ["#", "Issue", "Why it's a problem"],
        [
            ["1", "<code>pages/</code> used feature folders for <code>auth/</code> and <code>map/</code>, but four pages sat loose at the top level (<code>friends_page</code>, <code>profile_page</code>, <code>profile_edit_page</code>, <code>share_code_page</code>)", "The convention was half-applied; a reader can&rsquo;t tell whether features get a folder"],
            ["2", "<code>routing/</code> mixed real routing (<code>app_routing.dart</code>) with auth-gate-specific <em>pure logic</em> (<code>auth_gate_resolver.dart</code>, <code>deep_link_parser.dart</code>) used only by auth", "<code>routing/</code> wasn&rsquo;t cohesive; auth logic was misfiled"],
            ["3", "<code>service_provider.dart</code> (an InheritedWidget) lived in <code>services/</code> among plain-Dart service classes", "A kind-mismatch in the folder"],
            ["&mdash;", "The <code>auth/</code> folder had grown to 9 flat files", "Messy compared to <code>map/</code>&rsquo;s subfolders"],
        ]))

    b.append(h2("did", "2. What we did, and the reasoning"))
    b.append(h3("did1", "#1 — Group loose pages into feature folders"))
    b.append(code(r'''
pages/profile/  ← profile_page, profile_edit_page, share_code_page
pages/friends/  ← friends_page''', lang="text"))
    b.append('<p>Now every feature has a folder; the convention is consistent.</p>')
    b.append(h3("did2", "#2 — Move auth-gate logic OUT of routing/"))
    b.append('<p>A usage search confirmed these two helpers are consumed <strong>only</strong> by auth: '
             '<code>auth_gate_resolver.dart</code> (used only by <code>AuthGateModel</code>) and <code>deep_link_parser.dart</code> '
             '(used only by <code>ProfileLinkHolder</code>). So they moved next to their consumers, leaving '
             '<code>routing/app_routing.dart</code> as genuine navigation. This makes <code>routing/</code> cohesive and co-locates '
             'the auth-gate brains.</p>')
    b.append(h3("did3", "#3 — service_provider.dart placement (we weighed four homes)"))
    b.append(table(
        ["Option", "Where", "Verdict"],
        [
            ["A &mdash; leave it", "<code>services/</code>", "Defensible but mixes plain Dart + a widget"],
            ["B &mdash; DI folder", "<code>lib/di/</code>", "Cleanest signal; for a 2nd provider later"],
            ["C &mdash; app folder", "<code>lib/app/</code> (with <code>app.dart</code>)", CH() + " &mdash; both are top-level app wiring mounted at the root"],
            ["D &mdash; widgets folder", "<code>lib/widgets/</code>", "Mislabels DI as a generic widget"],
        ]))
    b.append(h3("byfeature", "Auth folder — why by-feature, not by-kind"))
    b.append('<p><code>map/</code> uses by-kind subfolders (<code>widgets/</code>, <code>renders/</code>, <code>models/</code>) because '
             'it&rsquo;s <em>one</em> screen with supporting parts. Auth is different &mdash; it has <strong>three distinct areas</strong> '
             '(gate, login, onboarding) &mdash; so by-sub-feature fits better than copying map&rsquo;s by-kind layout. We extracted the '
             'tightest, most-related cluster:</p>')
    b.append(code(r'''
pages/auth/gate/  ← auth_gate, auth_gate_model, auth_gate_resolver,
                     deep_link_parser, profile_link_holder''', lang="text"))
    b.append('<p><code>login/</code> and <code>onboarding/</code> were left flat &mdash; only two files each, not worth a folder yet '
             '(can split later for symmetry).</p>')

    b.append(h2("mechanics", "3. Mechanics — how the moves were done safely"))
    b.append('<ul>'
             '<li>Moved files with the filesystem; git detects renames at commit by content similarity, so history is preserved.</li>'
             '<li>For every move, searched for all imports (<code>package:</code> and relative) and updated them.</li>'
             '</ul>')
    b.append('<p><strong>Watch-outs that bit us:</strong></p>')
    b.append('<ul>'
             '<li>A test moved one level deeper, so its <em>relative</em> import to the shared fake had to gain a &ldquo;../&rdquo;: '
             '<code>../../services/...</code> &rarr; <code>../../../services/...</code></li>'
             '<li><code>deep_link_parser_test.dart</code> was an <strong>empty stub</strong> (no <code>main()</code>), which breaks the '
             'test runner (&ldquo;Undefined name &rsquo;main&rsquo;&rdquo;). We <em>filled</em> it with 5 real tests for '
             '<code>profileIdFromDeepLink</code> instead of leaving a broken file.</li>'
             '<li>After each batch: <code>flutter analyze lib test</code> (clean), then ran the gate tests.</li>'
             '</ul>')

    b.append(h2("layout", "4. Final layout (auth-relevant)"))
    b.append(code(r'''
lib/
├─ app/            app.dart, service_provider.dart
├─ pages/
│  ├─ auth/
│  │  ├─ gate/     auth_gate, auth_gate_model, auth_gate_resolver,
│  │  │            deep_link_parser, profile_link_holder
│  │  ├─ login_page, login_widgets
│  │  └─ onboarding_page, onboarding_widgets
│  ├─ map/
│  ├─ profile/     profile_page, profile_edit_page, share_code_page
│  └─ friends/     friends_page
├─ routing/        app_routing.dart  (navigation only)
└─ services/       auth_service (interface), supabase_auth_service, + others
test/pages/auth/gate/  mirrors gate/ (20 tests total, all passing)''', name="lib/ — final", lang="text"))

    b.append(h2("notdo", "5. What we deliberately did NOT do"))
    b.append('<ul>'
             '<li>Did not split <code>login/</code> and <code>onboarding/</code> into folders (2 files each; YAGNI).</li>'
             '<li>Did not adopt a global <code>domain/</code> vs <code>data/</code> split (over-engineering at this size).</li>'
             '<li>Did not move services into per-feature folders (the flat <code>services/</code> is fine for the current count).</li>'
             '</ul>')

    b.append(h2("result", "6. Result"))
    b.append('<ul>'
             '<li>The tree now answers &ldquo;is this codebase foldered-by-feature?&rdquo; with a clear <strong>yes</strong>.</li>'
             '<li><code>routing/</code> is honest (navigation only); auth-gate logic is one cohesive cluster.</li>'
             '<li><code>flutter analyze</code> clean; all 20 gate tests pass after the moves.</li>'
             '</ul>')
    b.append(callout("That&rsquo;s the whole refactor. Six commits, zero user-facing change, and an auth layer that is now testable, "
                     "diagnosable, consistent, and organized. Head back to the "
                     "<a href='index.html'><strong>Overview</strong></a> for the bird&rsquo;s-eye view.", "good", "Done:"))
    return "".join(b)
