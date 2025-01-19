export default [
    {
        path: '/',
        name: 'home',
        redirect: '/discover',
        children: [
            {
                path: 'discover',
                name: 'discover',
                component: () => import("../views/DiscoverView.vue")
            },

            {
                path: 'tending',
                name: 'tending',
                component: () => import("../views/TendingView.vue")
            },

        ]
    },
    {
        path: "/login",
        component: () => import("../views/Login.vue"),
    },
    {
        path: "/login_localstorage",
        component: () => import("../views/login_localstorage.vue"),
    },
    {
        path: "/table",
        component: () => import("../components/table.vue"),
    },
]
