import { BarChart3, Bell, CreditCard, Package, ShoppingCart, Users } from 'lucide-react'

const statCards = [
  { label: 'Orders today', value: '248', change: '+12.4%', icon: ShoppingCart },
  { label: 'Revenue', value: '$18.4K', change: '+8.1%', icon: CreditCard },
  { label: 'Guests served', value: '1,340', change: '+6.9%', icon: Users },
  { label: 'Inventory alerts', value: '14', change: '-2.4%', icon: Package },
]

export function DashboardPage() {
  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-col gap-4 rounded-2xl border border-slate-800 bg-slate-900/70 p-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-amber-400">Operations</p>
            <h1 className="mt-2 text-3xl font-bold">Restaurant Dashboard</h1>
          </div>

          <div className="flex items-center gap-3">
            <button className="rounded-lg border border-slate-700 bg-slate-800 p-2 text-slate-200">
              <Bell className="h-5 w-5" />
            </button>
            <button className="rounded-lg bg-amber-500 px-4 py-2 font-semibold text-slate-950 hover:bg-amber-400">
              New order
            </button>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {statCards.map(({ label, value, change, icon: Icon }) => (
            <div key={label} className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-lg shadow-slate-950/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-400">{label}</p>
                  <p className="mt-3 text-3xl font-bold">{value}</p>
                </div>
                <div className="rounded-xl bg-amber-500/10 p-3 text-amber-400">
                  <Icon className="h-6 w-6" />
                </div>
              </div>
              <p className="mt-4 text-sm text-emerald-400">{change} from yesterday</p>
            </div>
          ))}
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[2fr_1fr]">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Sales overview</h2>
              <div className="flex items-center gap-2 text-sm text-slate-400">
                <BarChart3 className="h-4 w-4" />
                Last 7 days
              </div>
            </div>

            <div className="grid min-h-64 place-items-center rounded-xl border border-dashed border-slate-700 bg-slate-950/60 text-slate-400">
              Recharts dashboard placeholder
            </div>
          </div>

          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h3 className="text-lg font-semibold">Live activity</h3>
              <div className="mt-4 space-y-3">
                {[
                  'Order #1042 accepted by kitchen',
                  'Table 12 requested assistance',
                  'Payment received for booking #44',
                ].map((item) => (
                  <div key={item} className="rounded-lg border border-slate-800 bg-slate-950 p-3 text-sm text-slate-300">
                    {item}
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h3 className="text-lg font-semibold">Quick actions</h3>
              <div className="mt-4 grid grid-cols-2 gap-3">
                {['Menu', 'Tables', 'Orders', 'Inventory'].map((action) => (
                  <button
                    key={action}
                    className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm font-medium text-slate-200 hover:border-amber-500"
                  >
                    {action}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
