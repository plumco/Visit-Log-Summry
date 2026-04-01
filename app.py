import React, { useState, useMemo } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Cell 
} from 'recharts';
import { 
  LayoutDashboard, 
  Building2, 
  MapPin, 
  FileText, 
  Clock, 
  TrendingUp, 
  TrendingDown,
  Users,
  Search,
  Download,
  Calendar,
  Filter
} from 'lucide-react';

const DATA_SET = {
  jan: [
    { id: 'Yash', floor: 87, site: 71, reportMark: 63, suggestion: 24, pending: 3, sent: 60, backlog: 0, total: 60 },
    { id: 'prath', floor: 97, site: 56, reportMark: 91, suggestion: 6, pending: 1, sent: 90, backlog: 0, total: 90 },
    { id: 'Jiten', floor: 29, site: 17, reportMark: 5, suggestion: 12, pending: 5, sent: 0, backlog: 0, total: 0 },
  ],
  feb: [
    { id: 'Yash', floor: 62, site: 57, reportMark: 36, suggestion: 22, pending: 4, sent: 35, backlog: 3, total: 38 },
    { id: 'prath', floor: 73, site: 59, reportMark: 51, suggestion: 8, pending: 9, sent: 58, backlog: 1, total: 59 },
    { id: 'Jiten', floor: 43, site: 31, reportMark: 2, suggestion: 29, pending: 0, sent: 2, backlog: 5, total: 7 },
    { id: 'Rutic', floor: 36, site: 36, reportMark: 14, suggestion: 22, pending: 1, sent: 13, backlog: 0, total: 13 },
    { id: 'Harsh', floor: 51, site: 35, reportMark: 15, suggestion: 20, pending: 0, sent: 26, backlog: 0, total: 26 },
  ],
  mar: [
    { id: 'Yash', floor: 43, site: 41, reportMark: 30, suggestion: 13, pending: 0, sent: 29, backlog: 4, total: 34 },
    { id: 'prath', floor: 53, site: 39, reportMark: 46, suggestion: 7, pending: 0, sent: 32, backlog: 9, total: 55 },
    { id: 'Jiten', floor: 31, site: 23, reportMark: 3, suggestion: 28, pending: 0, sent: 3, backlog: 0, total: 3 },
    { id: 'Rutic', floor: 23, site: 18, reportMark: 4, suggestion: 19, pending: 0, sent: 3, backlog: 1, total: 5 },
    { id: 'Harsh', floor: 55, site: 46, reportMark: 35, suggestion: 20, pending: 0, sent: 35, backlog: 0, total: 35 },
  ]
};

const StatCard = ({ title, value, icon: Icon, gradient, delta, isIncrease }) => (
  <div className="bg-white rounded-[2rem] p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-50 relative overflow-hidden group transition-all hover:shadow-xl">
    <div className="flex justify-between items-start mb-6">
      <div className={`p-4 rounded-2xl bg-gradient-to-br ${gradient} shadow-lg shadow-opacity-20`}>
        <Icon size={24} className="text-white" strokeWidth={2.5} />
      </div>
      <div className="text-right">
        <p className="text-slate-400 text-[10px] font-black uppercase tracking-[0.2em] mb-1">{title}</p>
        <h3 className="text-4xl font-black text-slate-800 tracking-tight">{value}</h3>
      </div>
    </div>
    <div className="flex items-center gap-2">
      {delta !== undefined ? (
        <>
          <span className="text-[10px] font-bold text-slate-300 uppercase">vs Last Month</span>
          <div className={`flex items-center gap-0.5 px-2.5 py-1 rounded-xl text-[11px] font-black ${isIncrease ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'}`}>
            {isIncrease ? <TrendingUp size={12} strokeWidth={3} /> : <TrendingDown size={12} strokeWidth={3} />}
            {delta}
          </div>
        </>
      ) : (
        <span className="text-[10px] font-bold text-slate-300 uppercase tracking-widest italic">Base Month</span>
      )}
    </div>
  </div>
);

const App = () => {
  const [activeTab, setActiveTab] = useState('mar');
  const [filterText, setFilterText] = useState('');

  const months = ['jan', 'feb', 'mar'];
  const currentData = useMemo(() => {
    return DATA_SET[activeTab].filter(item => 
      item.id.toLowerCase().includes(filterText.toLowerCase())
    );
  }, [activeTab, filterText]);

  const stats = useMemo(() => {
    const getTotals = (data) => data.reduce((acc, curr) => ({
      floor: acc.floor + curr.floor,
      site: acc.site + curr.site,
      reportMark: acc.reportMark + curr.reportMark,
      suggestion: acc.suggestion + curr.suggestion,
      pending: acc.pending + curr.pending,
      sent: acc.sent + curr.sent,
      backlog: acc.backlog + curr.backlog,
      total: acc.total + curr.total
    }), { floor: 0, site: 0, reportMark: 0, suggestion: 0, pending: 0, sent: 0, backlog: 0, total: 0 });

    const currentTotals = getTotals(DATA_SET[activeTab]);
    let deltas = null;

    const prevMonthIdx = months.indexOf(activeTab) - 1;
    if (prevMonthIdx >= 0) {
      const prevTotals = getTotals(DATA_SET[months[prevMonthIdx]]);
      deltas = {
        floor: currentTotals.floor - prevTotals.floor,
        site: currentTotals.site - prevTotals.site,
        total: currentTotals.total - prevTotals.total,
        pending: currentTotals.pending - prevTotals.pending
      };
    }

    return { totals: currentTotals, deltas };
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-[#F8FAFC] p-4 md:p-12 font-sans text-slate-800">
      <div className="max-w-[1400px] mx-auto space-y-10">
        
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
          <div className="flex items-center gap-6">
            <div className="bg-[#3B82F6] p-4 rounded-2xl shadow-xl shadow-blue-100">
              <LayoutDashboard className="text-white" size={32} strokeWidth={2.5} />
            </div>
            <div>
              <h1 className="text-4xl font-black tracking-tight text-slate-900 uppercase">Executive Dashboard</h1>
              <p className="text-slate-400 font-bold mt-2 text-sm uppercase tracking-widest flex items-center gap-2">
                <Calendar size={14} className="text-blue-500" />
                Performance Suite • {activeTab.toUpperCase()} 2024
              </p>
            </div>
          </div>

          <div className="flex bg-white p-1.5 rounded-[2rem] shadow-sm border border-slate-100">
            {months.map(m => (
              <button 
                key={m}
                onClick={() => setActiveTab(m)}
                className={`px-10 py-3 rounded-[1.5rem] text-xs font-black uppercase tracking-[0.2em] transition-all duration-300 ${activeTab === m ? 'bg-slate-900 text-white shadow-lg' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-50'}`}
              >
                {m}
              </button>
            ))}
          </div>
        </div>

        {/* KPI Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <StatCard 
            title="Total Tower Visits" 
            value={stats.totals.floor} 
            icon={Building2} 
            gradient="from-indigo-500 to-indigo-600"
            delta={stats.deltas ? Math.abs(stats.deltas.floor) : undefined}
            isIncrease={stats.deltas?.floor >= 0}
          />
          <StatCard 
            title="Total Site Visits" 
            value={stats.totals.site} 
            icon={MapPin} 
            gradient="from-emerald-500 to-emerald-600"
            delta={stats.deltas ? Math.abs(stats.deltas.site) : undefined}
            isIncrease={stats.deltas?.site >= 0}
          />
          <StatCard 
            title="Total Reports Sent" 
            value={stats.totals.total} 
            icon={FileText} 
            gradient="from-blue-500 to-blue-600"
            delta={stats.deltas ? Math.abs(stats.deltas.total) : undefined}
            isIncrease={stats.deltas?.total >= 0}
          />
          <StatCard 
            title="Pending Reports" 
            value={stats.totals.pending} 
            icon={Clock} 
            gradient="from-amber-500 to-amber-600"
            delta={stats.deltas ? Math.abs(stats.deltas.pending) : undefined}
            isIncrease={stats.deltas?.pending >= 0}
          />
        </div>

        {/* Visual Analytics */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          
          {/* Reports Sent Progress List */}
          <div className="lg:col-span-4 bg-white p-10 rounded-[3rem] shadow-[0_10px_40px_-15px_rgba(0,0,0,0.03)] border border-slate-50 h-[450px] flex flex-col">
            <div className="flex items-center justify-between mb-10">
              <h3 className="font-black text-slate-900 text-[10px] uppercase tracking-[0.25em] flex items-center gap-3">
                <div className="w-1.5 h-6 bg-blue-600 rounded-full"></div>
                Reports Sent Leaderboard
              </h3>
              <span className="bg-slate-100 text-slate-400 text-[9px] font-black px-3 py-1 rounded-full uppercase tracking-widest">{activeTab} '24</span>
            </div>
            <div className="space-y-8 overflow-y-auto pr-3 custom-scrollbar flex-grow">
              {currentData.sort((a, b) => b.total - a.total).map((item) => (
                <div key={item.id} className="group">
                  <div className="flex justify-between items-center text-[11px] font-black mb-3">
                    <span className="text-slate-600 uppercase group-hover:text-blue-600 transition-colors">{item.id}</span>
                    <span className="text-slate-400 font-bold">{item.total} REPORTS</span>
                  </div>
                  <div className="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
                    <div 
                      className="bg-[#3B82F6] h-full rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${(item.total / Math.max(...DATA_SET[activeTab].map(d => d.total || 1))) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tower vs Site Comparison Chart */}
          <div className="lg:col-span-8 bg-white p-10 rounded-[3rem] shadow-[0_10px_40px_-15px_rgba(0,0,0,0.03)] border border-slate-50 h-[450px]">
             <div className="flex items-center justify-between mb-10">
              <h3 className="font-black text-slate-900 text-[10px] uppercase tracking-[0.25em] flex items-center gap-3">
                <div className="w-1.5 h-6 bg-indigo-500 rounded-full"></div>
                Tower vs Site Activity Analysis
              </h3>
              <div className="flex gap-6">
                <div className="flex items-center gap-2 text-[9px] font-black uppercase text-slate-400 tracking-widest">
                  <div className="w-2.5 h-2.5 rounded-full bg-indigo-500"></div> Tower
                </div>
                <div className="flex items-center gap-2 text-[9px] font-black uppercase text-slate-400 tracking-widest">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div> Site
                </div>
              </div>
            </div>
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={currentData}
                  layout="vertical"
                  margin={{ top: 0, right: 30, left: 10, bottom: 0 }}
                  barGap={8}
                >
                  <XAxis type="number" hide />
                  <YAxis 
                    dataKey="id" 
                    type="category" 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 900 }}
                    width={80}
                  />
                  <Tooltip 
                    cursor={{ fill: '#F8FAFC', radius: 12 }}
                    contentStyle={{ borderRadius: '20px', border: 'none', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.1)', padding: '15px' }}
                  />
                  <Bar dataKey="floor" fill="#6366f1" radius={[0, 20, 20, 0]} barSize={10} name="Tower Visits" />
                  <Bar dataKey="site" fill="#10b981" radius={[0, 20, 20, 0]} barSize={10} name="Site Visits" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Detailed Data Ledger */}
        <div className="bg-white rounded-[3rem] shadow-[0_10px_40px_-15px_rgba(0,0,0,0.03)] border border-slate-50 overflow-hidden mb-16">
          <div className="px-10 py-8 border-b border-slate-50 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <h3 className="font-black text-slate-900 text-[10px] uppercase tracking-[0.3em]">Detailed Performance Breakdown</h3>
              <p className="text-slate-400 text-[11px] font-bold mt-1 uppercase tracking-tighter">Full ledger of associate outputs & conversions</p>
            </div>
            <div className="flex gap-4 w-full md:w-auto">
              <div className="relative flex-grow md:min-w-[280px]">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-300" size={16} />
                <input 
                  type="text" 
                  placeholder="FILTER ASSOCIATE NAME..." 
                  value={filterText}
                  onChange={(e) => setFilterText(e.target.value)}
                  className="pl-12 pr-6 py-3.5 bg-slate-50 border-none rounded-2xl text-[10px] font-black uppercase tracking-widest focus:ring-4 focus:ring-blue-50 outline-none w-full transition-all"
                />
              </div>
              <button className="p-3.5 bg-slate-900 text-white rounded-2xl hover:bg-black transition-all active:scale-95 shadow-xl shadow-slate-200">
                <Download size={20} strokeWidth={2.5} />
              </button>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/50 text-slate-400 text-[10px] font-black uppercase tracking-[0.25em]">
                  <th className="px-10 py-6">Associate ID</th>
                  <th className="px-6 py-6 text-center">Floor Visits</th>
                  <th className="px-6 py-6 text-center">Site Visits</th>
                  <th className="px-6 py-6 text-center">Mark (YES)</th>
                  <th className="px-6 py-6 text-center">Sugg (NO)</th>
                  <th className="px-6 py-6 text-center">Pending</th>
                  <th className="px-6 py-6 text-center">Sent</th>
                  {activeTab !== 'jan' && <th className="px-6 py-6 text-center text-blue-600">Backlog</th>}
                  <th className="px-10 py-6 text-right">Grand Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {currentData.map((row) => (
                  <tr key={row.id} className="group hover:bg-slate-50/50 transition-colors">
                    <td className="px-10 py-6 font-black text-slate-800 uppercase border-l-4 border-transparent group-hover:border-blue-600">{row.id}</td>
                    <td className="px-6 py-6 text-center text-slate-500 font-bold">{row.floor}</td>
                    <td className="px-6 py-6 text-center text-slate-500 font-bold">{row.site}</td>
                    <td className="px-6 py-6 text-center">
                      <span className="text-emerald-600 font-black px-3 py-1 bg-emerald-50 rounded-lg">{row.reportMark}</span>
                    </td>
                    <td className="px-6 py-6 text-center text-rose-400 font-bold">{row.suggestion}</td>
                    <td className="px-6 py-6 text-center">
                      <span className={`px-2.5 py-1 rounded-lg text-[10px] font-black ${row.pending > 0 ? 'bg-orange-50 text-orange-600 border border-orange-100' : 'text-slate-300'}`}>
                        {row.pending}
                      </span>
                    </td>
                    <td className="px-6 py-6 text-center text-slate-500 font-bold">{row.sent}</td>
                    {activeTab !== 'jan' && (
                      <td className="px-6 py-6 text-center">
                        <span className={`font-black ${row.backlog > 0 ? 'text-blue-500' : 'text-slate-200'}`}>
                          {row.backlog}
                        </span>
                      </td>
                    )}
                    <td className="px-10 py-6 text-right text-slate-900 font-black text-base">{row.total}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot className="bg-slate-900 text-white font-black">
                <tr>
                  <td className="px-10 py-8 uppercase tracking-[0.4em] text-[10px]">Team Aggregate</td>
                  <td className="px-6 py-8 text-center text-slate-400 font-black">{stats.totals.floor}</td>
                  <td className="px-6 py-8 text-center text-slate-400 font-black">{stats.totals.site}</td>
                  <td className="px-6 py-8 text-center text-emerald-400 font-black">{stats.totals.reportMark}</td>
                  <td className="px-6 py-8 text-center text-rose-400 font-black">{stats.totals.suggestion}</td>
                  <td className="px-6 py-8 text-center text-amber-400 font-black">{stats.totals.pending}</td>
                  <td className="px-6 py-8 text-center text-white">{stats.totals.sent}</td>
                  {activeTab !== 'jan' && <td className="px-6 py-8 text-center text-blue-400">{stats.totals.backlog}</td>}
                  <td className="px-10 py-8 text-right text-2xl text-blue-400 tracking-tighter">{stats.totals.total}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
