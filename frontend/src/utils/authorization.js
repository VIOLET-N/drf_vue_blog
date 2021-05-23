import axios from 'axios'

async function authorization() {
    const storage = localStorage;

    let hasLogin =  false;
    let username = storage.getItem('username.myblog');

    const expireTime = Number(storage.getItem('expiredTime.myblog'));
    const current = (new Date()).getTime();
    const refreshToken = storage.getItem('refresh.myblog');
    console.log('refresh', refreshToken);
    console.log('current', current);
    // 初始 Token 未过期
    if (expireTime > current) {
        hasLogin = true;
        console.log('authorization access 未过期')
    }
    // 初始 token 过期
    // 申请刷新
    else if (refreshToken !== null) {
        try {
            let response = await axios.post('/api/token/refresh/', {refresh: refreshToken});

            const nextExpiredTime = Date.parse(response.headers.date) + 60000;

            storage.setItem('access.myblog', response.data.access);
            storage.setItem('expiredTime.myblog', nextExpiredTime);
            storage.removeItem('refresh.myblog');

            hasLogin = true;

            console.log('authorization refresh 刷新');
            console.log('login expiredTime', nextExpiredTime)
        }
        catch (e) {
            storage.clear();
            hasLogin = false;
            console.log('authorization err 刷新失败')
        }
    }
    else {
        storage.clear();
        hasLogin = false;
        console.log('authorization exp 什么都没有')
    }
    console.log('authorization done');
    console.log(hasLogin, username);
    return [hasLogin, username]
}

export default authorization;