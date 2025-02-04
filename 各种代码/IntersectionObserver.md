[Vue2 中自定义图片懒加载指令 2.0](https://juejin.cn/post/7146659891300532232 "https://juejin.cn/post/7146659891300532232")

[IntersectionObserver的那一二件事 - 掘金](https://juejin.cn/post/7373858892038701067)

## IntersectionObserver 基础

**IntersectionObserver 可以监听一个元素和可视区域相交部分的比例，然后在可视比例达到某个阈值的时候触发回调。比如可以用来处理图片的懒加载等等**

**首先我们来看下基本的格式：**

```js
const observer = new IntersectionObserver(callback, [options]);
```

**相关的API属性和方法：**

直接看他的Typescript结构吧

```ts
interface IntersectionObserver {
    // root 属性用来获取当前 intersectionObserver 实例的根元素
    readonly root: Element | Document | null;
   
    readonly rootMargin: string;
    
    readonly thresholds: ReadonlyArray<number>;
    
    disconnect(): void;
   
    observe(target: Element): void;
   
    takeRecords(): IntersectionObserverEntry[];
    
    unobserve(target: Element): void;
}

```

`root`: 如果构造函数未传入 `root` 或其值为 `null`，则默认使用**顶级当前文档**的视口。

`rootMargin` ： 是 `IntersectionObserver` 构造函数的一个可选属性，它定义了一个矩形区域，用于扩展或缩小 `root`元素的可视区域，从而影响 `intersectionRatio`的计算

```js
const observer = new IntersectionObserver(
  entries => {
    // 处理entries
  },
  {
    root: document.querySelector('#scrollArea'), // 根元素 || 顶级当前文档
    rootMargin: '50px 20px 30px 10px' // 上右下左
  }
);

```

`thresholds`：，它定义了一个监听交叉变化时触发回调的阈值列表。这些阈值是介于0和1之间的数值，包括0和1，表示目标元素与根元素相交的比例。举个例子，当创建一个 `IntersectionObserver`实例时，你可以指定一个或多个阈值。例如，如果你想要在目标元素至少有25%、50%和75%可见时触发回调，你可以这样设置 `thresholds`

```js
const observer = new IntersectionObserver(
  entries => {
    // 处理entries
  },
  {
    thresholds: [0, 0.25, 0.5, 0.75, 1]
  }
);

```

`disconnect`用于停止监听目标元素与根元素的交叉变化。当你不再需要观察元素的可见性变化时，可以调用 `disconnect`方法来停止 `IntersectionObserver`的所有活动。

调用 `disconnect`方法后，`IntersectionObserver`将不再触发任何回调，即使目标元素的可见性发生变化。这意味着，你已经不再对目标元素的可见性感兴趣，或者你想要在组件卸载时清理资源。

```js
// 创建一个IntersectionObserver实例
const observer = new IntersectionObserver(function(entries) {
  // 处理交叉变化
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      console.log('元素现在可见');
    } else {
      console.log('元素不再可见');
    }
  });
});

// 开始观察一个元素
const target = document.querySelector('#my-element');
observer.observe(target);

// ...一段时间后...

// 停止观察元素
observer.disconnect();

```

`observer`: 用于开始监听一个目标元素与根元素的交叉变化。当你想要知道一个元素是否进入了视口（即用户的可见区域）时，你可以使用 `observe`方法来指定需要观察的元素

```js
// 创建一个IntersectionObserver实例
const observer = new IntersectionObserver(function(entries) {
  // 处理交叉变化
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      console.log('元素现在可见');
    } else {
      console.log('元素不再可见');
    }
  });
});

// 获取要观察的元素
const target = document.querySelector('#my-element');

// 开始观察元素
observer.observe(target);

```

`takeRecords`:用于获取并清空 `IntersectionObserver`实例的记录队列。这个方法返回一个 `IntersectionObserverEntry`对象的数组，每个对象描述了目标元素的相交状态

`unobserve`:用于停止监听特定目标元素与根元素的交叉变化。当你不再需要监听某个元素的可见性变化时，你可以使用 `unobserve`方法来停止对该元素的观察。

## 综合案例，实现图片的懒加载

下面的方法使用的react，可以做必要的安装哦！

下面是一个设置一个组件，看如下代码

```ts
/*
 * @Date: 2024-05-28 09:59:48
 * @Description: 组件的设计
 */
import { CSSProperties, FC, ReactNode, useEffect, useRef, useState } from "react";

interface MyLazyloadProps {
  className?: string; /* className 和 style 是给外层 div 添加样式的 */
  style?: CSSProperties;
  placeholder?: ReactNode; /* 是占位的内容 */
  offset?: string | number; /* 是距离到可视区域多远就触发加载 */
  width?: number | string;
  height?: string | number;
  onContentVisible?: () => void; /* 进入可视化区域后所产生的回调 */
  children: ReactNode;
}

const MyLazyload: FC<MyLazyloadProps> = (props) => {
  const { className = "", style, offset = 0, width, onContentVisible, placeholder, height, children } = props;

  const containerRef = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  const elementObserver = useRef<IntersectionObserver>();

  /* 关键函数去判断可视范围 */
  const lazyLoadHandler = (entries: IntersectionObserverEntry[]) => {

    const [entry] = entries;
    const { isIntersecting, intersectionRatio } = entry;
    
    if (intersectionRatio > 0) {
      const node = containerRef.current;
      console.log(node, entry, intersectionRatio);
    }

    if (isIntersecting) {
      setVisible(true);
      /* 可以通过这一层函数传递给外部，然后通过这个函数，可以在外部组件做相对应的处理等等 */
      onContentVisible?.();

      const node = containerRef.current;
      // 展示完成后及时的销毁
      if (node && node instanceof HTMLElement) {
        elementObserver.current?.unobserve(node);
      }
    }
  }

  useEffect(() => {
    const options = {
        /* 这边没有写root，则这边的根元素就是此文档的 containerRef */
        /* rootMargin 这边做了一次偏移处理 */
        rootMargin: typeof offset === 'number' ? `${offset}px` : offset || '0px',
        /* 设置 threshold 为 0 也就是一进入可视区域就触发 */
        threshold: 0,
    }

    elementObserver.current = new IntersectionObserver(lazyLoadHandler, options);

    const node = containerRef.current; // 拿到node

    if (node instanceof HTMLElement) {
        elementObserver.current.observe(node);
    }
    return () => {
        if (node && node instanceof HTMLElement) {
            elementObserver.current?.unobserve(node);
        }
    }
  }, []);

  const styles = { height, width, ...style };

  return (
    <div ref={containerRef} className={`${className}`} style={styles}>
      {visible ? children : placeholder}
    </div>
  );
};

export default MyLazyload;



```

组件的调用：

```js
/*
 * @Date: 2024-05-27 11:21:07
 * @Description: 组件的调用
 */
import { useState } from "react";
import img1 from "./素材1.png";
import img2 from "./扑克牌1.jpg";
import "./App.css";
// import LazyLoad from 'react-lazyload';
import LazyLoad from "./MyLazyLoad";

function App() {
  const [isVisible, setIsVisible] = useState<boolean>(false);
  return (
    <div>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      <p>一一一一一一一一一一一一一一一一一一</p>
      {/* 这边增加一些类名可以做一些的动画 */}
      <LazyLoad
        className={isVisible ? "show" : "hide"}
        placeholder={<div>loading...</div>}
        onContentVisible={() => {
          console.log("comp visible");
          setIsVisible(true);
        }}
      >
        {/* <img src={img1}/> */}
      </LazyLoad>
      <LazyLoad
        placeholder={<div>loading...</div>}
        onContentVisible={() => {
          console.log("img visible");
        }}
      >
        <img src={img2} />
      </LazyLoad>
    </div>
  );
}

export default App;


```

我们看最后的效果：

当刚进入页面的时候，我们下面的元素都处于 loading中，也是上面的placeholder的占位内容。

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/06c6ee04910f40778f5d92649f10af02~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=707&h=342&s=30907&e=png&b=fdfdfd)

当滑动图片的位置的时候才加载出相对应的图片地址和对应的类名

![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b73542ba68ef4bb1b8008e2e4294f490~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=720&h=410&s=348080&e=png&b=f4f0ef)

作者：小前端爱coding
链接：https://juejin.cn/post/7373858892038701067
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
