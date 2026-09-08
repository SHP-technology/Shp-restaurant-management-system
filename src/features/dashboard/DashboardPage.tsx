import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard,
  ShoppingBag,
  Grid,
  Calendar,
  Truck,
  PartyPopper,
  UtensilsCrossed,
  Users,
  BarChart2,
  Settings as SettingsIcon,
  LogOut,
  ChevronDown,
  TrendingUp,
  Download,
  Edit2,
  Trash2,
} from 'lucide-react'
import { useAuthStore } from '../../store/authStore'

export function DashboardPage() {
  const clearSession = useAuthStore((state) => state.clearSession)
  const navigate = useNavigate()

  const [activeTab, setActiveTab] = useState('Dashboard')
  const [orderFilter, setOrderFilter] = useState('All')

  const handleLogout = () => {
    clearSession()
    navigate('/')
  }

  // Sidebar items matching the exact screenshot
  const sidebarItems = [
    { name: 'Dashboard', icon: LayoutDashboard, badge: null },
    { name: 'Orders', icon: ShoppingBag, badge: '6' },
    { name: 'Table Management', icon: Grid, badge: null },
    { name: 'Reservations', icon: Calendar, badge: null },
    { name: 'Delivery Orders', icon: Truck, badge: null },
    { name: 'Party Bookings', icon: PartyPopper, badge: null },
    { name: 'Menu Management', icon: UtensilsCrossed, badge: null },
    { name: 'Customers', icon: Users, badge: null },
    { name: 'Reports', icon: BarChart2, badge: null },
    { name: 'Settings', icon: SettingsIcon, badge: null },
  ]

  // Dashboard Stats
  const stats = [
    { label: "Today's Orders", value: '54', sub1: '+12%', sub2: '+2%' },
    { label: 'Table Bookings', value: '18', sub1: '+0%', sub2: '-1%' },
    { label: 'Delivery Orders', value: '32', sub1: '+10%', sub2: '+18%' },
    { label: 'Party Bookings', value: '06', sub1: '+5%', sub2: '-1%' },
  ]

  // Live Orders
  const liveOrders = [
    { id: '#1258', type: 'Dine In', items: '2 items • Truffle Pizza, Lemonade', customer: 'Table 4 (Rahul M.)', price: '₹458', status: 'New', statusColor: 'bg-blue-100 text-blue-700' },
    { id: '#1257', type: 'Delivery', items: '3 items • Veg Biryani, Lava Cake', customer: 'Harsh P. (Civil Lines)', price: '₹678', status: 'Preparing', statusColor: 'bg-[#f47b20]/20 text-[#f47b20]' },
    { id: '#1256', type: 'Dine In', items: '1 item • Burrata Margherita', customer: 'Table 12 (Ananya R.)', price: '₹249', status: 'Ready', statusColor: 'bg-emerald-100 text-emerald-700' },
    { id: '#1255', type: 'Delivery', items: '4 items • Smash Burgers, Fries', customer: 'Vikram S. (Sunset Towers)', price: '₹689', status: 'New', statusColor: 'bg-blue-100 text-blue-700' },
    { id: '#1254', type: 'Takeaway', items: '2 items • Schezwan Noodles', customer: 'Priya K.', price: '₹378', status: 'Preparing', statusColor: 'bg-amber-100 text-amber-700' },
    { id: '#1253', type: 'Dine In', items: '3 items • Pasta, Garlic Bread', customer: 'Table 1 (Amit K.)', price: '₹520', status: 'Completed', statusColor: 'bg-gray-100 text-gray-700' },
  ]

  // Table Management State
  const [tableList, setTableList] = useState(
    Array.from({ length: 16 }, (_, i) => {
      const num = i + 1
      let status = 'Available'
      if (num === 5 || num === 7) status = 'Booked'
      if (num === 3 || num === 12) status = 'Occupied'
      const seats = num % 3 === 0 ? 6 : num % 2 === 0 ? 4 : 2
      return { num, status, seats }
    })
  )

  const toggleTableStatus = (num: number) => {
    setTableList((prev) =>
      prev.map((t) => {
        if (t.num === num) {
          const nextStatus = t.status === 'Available' ? 'Booked' : t.status === 'Booked' ? 'Occupied' : 'Available'
          return { ...t, status: nextStatus }
        }
        return t
      })
    )
  }

  // Reservations State
  const reservations = [
    { id: 'RES-101', name: 'Harsh Patel', phone: '+91 98765 43210', date: '28 May 2025', time: '7:30 PM', guests: '4 People', area: 'Indoor (Table 5)', status: 'Confirmed' },
    { id: 'RES-102', name: 'Neha Sharma', phone: '+91 98123 45678', date: '28 May 2025', time: '8:15 PM', guests: '2 People', area: 'Rooftop', status: 'Pending' },
    { id: 'RES-103', name: 'Karan Mehra', phone: '+91 99887 76655', date: '29 May 2025', time: '1:30 PM', guests: '6 People', area: 'VIP Booth', status: 'Confirmed' },
  ]

  // Delivery Orders State
  const deliveryList = [
    { id: '#DEL-801', customer: 'Rohan Gupta', phone: '+91 98765 11223', address: 'Flat 302, Green Park', status: 'Out for Delivery', driver: 'Suresh (Rider #4)', time: '20 mins left' },
    { id: '#DEL-802', customer: 'Sneha Roy', phone: '+91 98111 22334', address: 'B-12, Model Town', status: 'Preparing', driver: 'Assigning...', time: '35 mins left' },
    { id: '#DEL-803', customer: 'Aman Verma', phone: '+91 97777 88899', address: 'Suite 401, Tech Hub', status: 'Delivered', driver: 'Ramesh (Rider #1)', time: 'Completed' },
  ]

  // Party Bookings State
  const parties = [
    { id: 'PRT-501', occasion: 'Birthday Bash', client: 'Pooja Kapoor', date: '05 June 2025', guests: '20 People', requirements: 'Decoration, Cake, Music', status: 'Confirmed' },
    { id: 'PRT-502', occasion: 'Corporate Gala', client: 'TechCorp Solutions', date: '12 June 2025', guests: '50 People', requirements: 'Private Hall & Cocktail Bar', status: 'Pending Inquiry' },
  ]

  // Menu Management State
  const menuItems = [
    { id: 1, name: 'Truffle Mushroom Pizza', category: 'Pizza', price: 349, status: 'In Stock' },
    { id: 2, name: 'Artisan Smash Burger', category: 'Burgers', price: 279, status: 'In Stock' },
    { id: 3, name: 'Dum Pukht Veg Biryani', category: 'Indian', price: 299, status: 'In Stock' },
    { id: 4, name: 'Spicy Schezwan Noodles', category: 'Chinese', price: 249, status: 'In Stock' },
    { id: 5, name: 'Matcha Citrus Sparkler', category: 'Beverages', price: 169, status: 'Out of Stock' },
  ]

  // Customers State
  const customers = [
    { id: 'CUST-01', name: 'Harsh Patel', phone: '+91 98765 43210', visits: 14, totalSpent: '₹12,450', tag: 'VIP' },
    { id: 'CUST-02', name: 'Ananya Rao', phone: '+91 98123 45678', visits: 8, totalSpent: '₹6,800', tag: 'Regular' },
    { id: 'CUST-03', name: 'Vikram Singh', phone: '+91 99887 11223', visits: 3, totalSpent: '₹2,350', tag: 'New' },
  ]

  // Settings State
  const [outletName, setOutletName] = useState('SHP Restaurant - Civil Lines')
  const [gstRate, setGstRate] = useState('5%')
  const [autoAccept, setAutoAccept] = useState(true)

  return (
    <div className="min-h-screen bg-[#f4f3ef] text-[#1d211e] flex flex-col md:flex-row font-sans">
      {/* Left Dark Sidebar - Exact styling matching the attached image */}
      <aside className="w-full md:w-64 bg-[#141312] text-white flex flex-col justify-between p-4 shrink-0 shadow-2xl">
        <div>
          {/* Logo Brand */}
          <div className="flex items-center justify-between pb-6 border-b border-gray-800">
            <Link to="/" className="flex items-center gap-2.5">
              <img src="/logo.png" alt="SHP Logo" className="h-8 w-8 rounded-lg object-cover" />
              <span className="font-heading text-xl font-bold tracking-tight text-white">
                SHP
              </span>
            </Link>
            <Link to="/" className="text-[10px] text-gray-400 hover:text-white underline">
              View Website
            </Link>
          </div>

          {/* Navigation items list */}
          <nav className="mt-4 space-y-1 text-xs">
            {sidebarItems.map((item) => {
              const Icon = item.icon
              const isActive = activeTab === item.name
              return (
                <button
                  key={item.name}
                  onClick={() => setActiveTab(item.name)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition font-medium ${
                    isActive
                      ? 'bg-[#f47b20] text-white font-bold shadow-md'
                      : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon size={16} />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span className="rounded-full bg-rose-500 px-1.5 py-0.5 text-[9px] font-bold text-white">
                      {item.badge}
                    </span>
                  )}
                </button>
              )
            })}
          </nav>
        </div>

        {/* Logout */}
        <div className="pt-4 border-t border-gray-800">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold text-gray-400 hover:text-rose-400 transition"
          >
            <LogOut size={16} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-4 sm:p-6 lg:p-8 space-y-6 overflow-x-hidden">
        {/* Header Bar */}
        <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-[#f47b20]">Outlet Panel</span>
              <span className="text-gray-300">•</span>
              <span className="text-xs font-semibold text-gray-600">{activeTab}</span>
            </div>
            <h1 className="font-heading text-xl font-bold text-gray-900 mt-0.5">{activeTab} Section</h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 px-3 py-1.5 rounded-lg text-xs font-bold text-gray-700">
              <span>28 May 2025</span>
              <ChevronDown size={14} />
            </div>

            <span className="rounded-full bg-emerald-100 text-emerald-700 px-3 py-1 text-xs font-bold flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-emerald-600 animate-pulse" /> Live Outlet Status
            </span>
          </div>
        </header>

        {/* =========================================================
            TAB 1: DASHBOARD (Default view matching Outlet Panel Image)
        ========================================================= */}
        {activeTab === 'Dashboard' && (
          <div className="space-y-6">
            {/* Top 4 Stat Cards */}
            <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              {stats.map((stat) => (
                <div key={stat.label} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                  <p className="text-[11px] font-bold text-gray-500 uppercase tracking-wider">{stat.label}</p>
                  <p className="text-2xl font-black text-gray-900 mt-1">{stat.value}</p>
                  <div className="flex items-center gap-2 mt-2 text-[10px] font-bold">
                    <span className="text-emerald-600">{stat.sub1}</span>
                    <span className="text-gray-400">{stat.sub2}</span>
                  </div>
                </div>
              ))}
            </section>

            {/* Live Orders & Table Status Grid */}
            <section className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Live Orders */}
              <div className="lg:col-span-6 bg-white p-4 sm:p-5 rounded-xl border border-gray-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between border-b pb-3">
                  <h2 className="font-heading text-base font-bold text-gray-900">Live Orders</h2>
                  <div className="flex items-center gap-1 text-[11px] font-bold text-gray-600 bg-gray-100 p-1 rounded-lg">
                    {['All', 'Dine In', 'Delivery', 'Takeaway'].map((f) => (
                      <button
                        key={f}
                        onClick={() => setOrderFilter(f)}
                        className={`px-2.5 py-1 rounded-md transition ${
                          orderFilter === f ? 'bg-white text-[#f47b20] shadow-sm font-bold' : 'hover:text-gray-900'
                        }`}
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="space-y-2.5">
                  {liveOrders
                    .filter((o) => orderFilter === 'All' || o.type === orderFilter)
                    .map((order) => (
                      <div key={order.id} className="flex items-center justify-between p-3 rounded-lg border border-gray-100 bg-gray-50 hover:bg-white transition text-xs">
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-gray-900">{order.id}</span>
                            <span className="text-gray-500 font-medium">{order.type}</span>
                          </div>
                          <p className="text-[11px] text-gray-500 mt-0.5">{order.items}</p>
                        </div>
                        <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold ${order.statusColor}`}>
                          {order.status}
                        </span>
                      </div>
                    ))}
                </div>
              </div>

              {/* Table Status */}
              <div className="lg:col-span-6 space-y-6">
                <div className="bg-white p-4 sm:p-5 rounded-xl border border-gray-200 shadow-sm space-y-4">
                  <div className="flex items-center justify-between border-b pb-3">
                    <h2 className="font-heading text-base font-bold text-gray-900">Table Status</h2>
                    <div className="flex items-center gap-3 text-[10px] font-bold">
                      <span className="text-emerald-600">● Available</span>
                      <span className="text-[#f47b20]">● Booked</span>
                      <span className="text-rose-600">● Occupied</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-2.5">
                    {tableList.map((t) => (
                      <button
                        key={t.num}
                        onClick={() => toggleTableStatus(t.num)}
                        className={`h-12 rounded-lg flex flex-col items-center justify-center font-bold text-xs border transition ${
                          t.status === 'Booked'
                            ? 'bg-[#f47b20] text-white border-[#f47b20]'
                            : t.status === 'Occupied'
                            ? 'bg-rose-500 text-white border-rose-500'
                            : 'bg-white text-gray-700 border-gray-300 hover:border-emerald-500'
                        }`}
                      >
                        <span>{t.num}</span>
                        <span className="text-[9px] opacity-80">{t.seats} Seats</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">Today's Revenue</p>
                    <p className="text-2xl font-black text-gray-900 mt-1">₹28,450</p>
                  </div>
                  <div className="flex items-center gap-1.5 text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-lg text-xs font-bold border border-emerald-200">
                    <TrendingUp size={16} />
                    <span>+15% vs yesterday</span>
                  </div>
                </div>
              </div>
            </section>
          </div>
        )}

        {/* =========================================================
            TAB 2: ORDERS
        ========================================================= */}
        {activeTab === 'Orders' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b pb-4">
              <h2 className="font-heading text-lg font-bold text-gray-900">All Kitchen & POS Orders</h2>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  placeholder="Search order ID..."
                  className="rounded-md border border-gray-300 px-3 py-1.5 text-xs focus:border-[#f47b20] focus:outline-none"
                />
                <button className="rounded-md bg-[#f47b20] px-4 py-1.5 text-xs font-bold text-white">
                  + POS Order
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b bg-gray-50 text-gray-600 uppercase font-bold">
                    <th className="p-3">Order ID</th>
                    <th className="p-3">Customer / Table</th>
                    <th className="p-3">Items</th>
                    <th className="p-3">Type</th>
                    <th className="p-3">Total</th>
                    <th className="p-3">Status</th>
                    <th className="p-3">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {liveOrders.map((o) => (
                    <tr key={o.id} className="hover:bg-gray-50">
                      <td className="p-3 font-bold text-gray-900">{o.id}</td>
                      <td className="p-3 font-medium text-gray-700">{o.customer}</td>
                      <td className="p-3 text-gray-600">{o.items}</td>
                      <td className="p-3 text-gray-500 font-semibold">{o.type}</td>
                      <td className="p-3 font-bold text-[#f47b20]">{o.price}</td>
                      <td className="p-3">
                        <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold ${o.statusColor}`}>
                          {o.status}
                        </span>
                      </td>
                      <td className="p-3">
                        <button className="rounded bg-gray-900 px-2.5 py-1 text-[10px] font-bold text-white hover:bg-[#f47b20]">
                          Update Status
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 3: TABLE MANAGEMENT
        ========================================================= */}
        {activeTab === 'Table Management' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b pb-4">
              <div>
                <h2 className="font-heading text-lg font-bold text-gray-900">Floor Layout & Table Control</h2>
                <p className="text-xs text-gray-500">Click any table tile to cycle status (Available $\rightarrow$ Booked $\rightarrow$ Occupied)</p>
              </div>

              <div className="flex items-center gap-4 text-xs font-bold">
                <span className="flex items-center gap-1 text-emerald-600"><span className="h-3 w-3 rounded-full bg-emerald-500" /> Available (12)</span>
                <span className="flex items-center gap-1 text-[#f47b20]"><span className="h-3 w-3 rounded-full bg-[#f47b20]" /> Booked (2)</span>
                <span className="flex items-center gap-1 text-rose-600"><span className="h-3 w-3 rounded-full bg-rose-500" /> Occupied (2)</span>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-4 gap-4">
              {tableList.map((t) => (
                <div
                  key={t.num}
                  onClick={() => toggleTableStatus(t.num)}
                  className={`cursor-pointer rounded-xl border-2 p-5 flex flex-col justify-between h-32 transition shadow-sm ${
                    t.status === 'Booked'
                      ? 'bg-orange-50 border-[#f47b20] text-[#f47b20]'
                      : t.status === 'Occupied'
                      ? 'bg-rose-50 border-rose-500 text-rose-700'
                      : 'bg-white border-emerald-500 text-emerald-800 hover:shadow-md'
                  }`}
                >
                  <div className="flex justify-between items-center font-bold">
                    <span className="text-base">Table {t.num}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-white/80 border font-bold">{t.seats} Seater</span>
                  </div>
                  <div>
                    <span className="text-xs font-black uppercase tracking-wider">{t.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 4: RESERVATIONS
        ========================================================= */}
        {activeTab === 'Reservations' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b pb-4">
              <h2 className="font-heading text-lg font-bold text-gray-900">Table Reservation Log</h2>
              <button className="rounded-md bg-[#f47b20] px-4 py-2 text-xs font-bold text-white">
                + New Reservation
              </button>
            </div>

            <div className="space-y-3">
              {reservations.map((res) => (
                <div key={res.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-gray-200 bg-gray-50 gap-4 text-xs">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-900 text-sm">{res.name}</span>
                      <span className="text-gray-500 font-mono">({res.phone})</span>
                      <span className="rounded bg-orange-100 text-[#f47b20] px-2 py-0.5 text-[10px] font-bold">{res.id}</span>
                    </div>
                    <p className="text-gray-600 mt-1">
                      📅 {res.date} • 🕒 {res.time} • 👥 {res.guests} • 🪑 {res.area}
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      res.status === 'Confirmed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {res.status}
                    </span>
                    <button className="rounded border border-gray-300 px-3 py-1.5 text-xs font-bold text-gray-700 hover:bg-gray-100">
                      Assign Table
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 5: DELIVERY ORDERS
        ========================================================= */}
        {activeTab === 'Delivery Orders' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <h2 className="font-heading text-lg font-bold text-gray-900 border-b pb-4">Doorstep Delivery Logistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {deliveryList.map((del) => (
                <div key={del.id} className="rounded-xl border border-gray-200 p-4 space-y-3 bg-gray-50">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-gray-900">{del.id}</span>
                    <span className="rounded bg-blue-100 text-blue-700 px-2 py-0.5 text-[10px] font-bold">{del.status}</span>
                  </div>
                  <p className="text-xs font-bold text-gray-800">{del.customer} ({del.phone})</p>
                  <p className="text-xs text-gray-500">📍 {del.address}</p>
                  <div className="pt-2 border-t flex justify-between items-center text-xs">
                    <span className="text-gray-600 font-medium">🛵 {del.driver}</span>
                    <span className="text-[#f47b20] font-bold">{del.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 6: PARTY BOOKINGS
        ========================================================= */}
        {activeTab === 'Party Bookings' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <h2 className="font-heading text-lg font-bold text-gray-900 border-b pb-4">Party & Celebration Requests</h2>
            <div className="space-y-3">
              {parties.map((p) => (
                <div key={p.id} className="p-4 rounded-xl border border-gray-200 bg-orange-50/40 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-xs">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-base text-gray-900">{p.occasion}</span>
                      <span className="rounded bg-[#f47b20] text-white px-2 py-0.5 text-[10px] font-bold">{p.id}</span>
                    </div>
                    <p className="text-gray-700 font-semibold mt-1">Client: {p.client} • Date: {p.date} • Guests: {p.guests}</p>
                    <p className="text-gray-500 text-[11px] mt-0.5">Requirements: {p.requirements}</p>
                  </div>
                  <span className="px-3 py-1 rounded-md bg-emerald-100 text-emerald-700 font-bold text-xs">
                    {p.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 7: MENU MANAGEMENT
        ========================================================= */}
        {activeTab === 'Menu Management' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b pb-4">
              <h2 className="font-heading text-lg font-bold text-gray-900">Food Menu Catalog Editor</h2>
              <button className="rounded-md bg-[#f47b20] px-4 py-2 text-xs font-bold text-white">
                + Add New Dish
              </button>
            </div>

            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b bg-gray-50 text-gray-600 font-bold uppercase">
                  <th className="p-3">Dish Name</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Price</th>
                  <th className="p-3">Stock Status</th>
                  <th className="p-3">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {menuItems.map((item) => (
                  <tr key={item.id}>
                    <td className="p-3 font-bold text-gray-900">{item.name}</td>
                    <td className="p-3 text-gray-600">{item.category}</td>
                    <td className="p-3 font-bold text-[#f47b20]">₹{item.price}</td>
                    <td className="p-3">
                      <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold ${
                        item.status === 'In Stock' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="p-3 flex items-center gap-2">
                      <button className="p-1 text-gray-600 hover:text-[#f47b20]"><Edit2 size={14} /></button>
                      <button className="p-1 text-gray-600 hover:text-rose-600"><Trash2 size={14} /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* =========================================================
            TAB 8: CUSTOMERS
        ========================================================= */}
        {activeTab === 'Customers' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <h2 className="font-heading text-lg font-bold text-gray-900 border-b pb-4">Customer Directory & Loyalty</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {customers.map((c) => (
                <div key={c.id} className="p-4 rounded-xl border border-gray-200 bg-gray-50 space-y-2 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-gray-900">{c.name}</span>
                    <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-700 font-bold text-[10px]">{c.tag}</span>
                  </div>
                  <p className="text-gray-500">📞 {c.phone}</p>
                  <div className="pt-2 border-t flex justify-between text-gray-700 font-semibold">
                    <span>Visits: {c.visits}</span>
                    <span className="text-[#f47b20] font-bold">Total: {c.totalSpent}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 9: REPORTS (Highlighted in Screenshot)
        ========================================================= */}
        {activeTab === 'Reports' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b pb-4">
              <div>
                <h2 className="font-heading text-lg font-bold text-gray-900">Analytics & Sales Reports</h2>
                <p className="text-xs text-gray-500">Comprehensive breakdown of sales revenue, orders & category performance.</p>
              </div>

              <button className="flex items-center gap-1.5 rounded-md bg-[#f47b20] px-4 py-2 text-xs font-bold text-white hover:bg-[#d9630f] transition">
                <Download size={14} /> Export Report (CSV)
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200">
                <p className="text-xs font-bold text-gray-500 uppercase">Monthly Revenue</p>
                <p className="text-2xl font-black text-gray-900 mt-1">₹8,54,200</p>
                <p className="text-xs text-emerald-600 font-bold mt-1">+18.5% growth</p>
              </div>
              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200">
                <p className="text-xs font-bold text-gray-500 uppercase">Average Order Value</p>
                <p className="text-2xl font-black text-gray-900 mt-1">₹526</p>
                <p className="text-xs text-emerald-600 font-bold mt-1">+4.2% from last week</p>
              </div>
              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200">
                <p className="text-xs font-bold text-gray-500 uppercase">Top Selling Category</p>
                <p className="text-2xl font-black text-[#f47b20] mt-1">Pizza & Burgers</p>
                <p className="text-xs text-gray-500 font-medium mt-1">42% total sales share</p>
              </div>
            </div>
          </div>
        )}

        {/* =========================================================
            TAB 10: SETTINGS
        ========================================================= */}
        {activeTab === 'Settings' && (
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-6 max-w-3xl">
            <h2 className="font-heading text-lg font-bold text-gray-900 border-b pb-4">Outlet Settings & Configuration</h2>

            <div className="space-y-4 text-xs">
              <div>
                <label className="font-bold text-gray-700 block mb-1">Outlet Name</label>
                <input
                  type="text"
                  value={outletName}
                  onChange={(e) => setOutletName(e.target.value)}
                  className="w-full rounded-md border border-gray-300 p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                />
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">Default Tax / GST Rate</label>
                <input
                  type="text"
                  value={gstRate}
                  onChange={(e) => setGstRate(e.target.value)}
                  className="w-full rounded-md border border-gray-300 p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border border-gray-200 bg-gray-50">
                <div>
                  <p className="font-bold text-gray-900">Auto-accept Online Delivery Orders</p>
                  <p className="text-[11px] text-gray-500">Automatically send incoming online orders to kitchen queue</p>
                </div>
                <input
                  type="checkbox"
                  checked={autoAccept}
                  onChange={() => setAutoAccept(!autoAccept)}
                  className="h-5 w-5 accent-[#f47b20] cursor-pointer"
                />
              </div>

              <button className="rounded-md bg-[#f47b20] px-6 py-2.5 text-xs font-bold text-white hover:bg-[#d9630f]">
                Save Settings
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
