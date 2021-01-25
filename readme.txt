黃隊->藍色球門方向: 0, 1, 0 (x, y, z) 1.57(rad)
藍隊->黃色球門方向: 0,-1, 0 (x, y, z) 1.57(rad)
車子大小: 0.75*0.75*0.75 (x * y * z)
輪子大小: 0.02*0.01 (r * h)
最大速度: 10 (rad/s)

車子感應器: 左輪轉動(left wheel motor)      右輪轉動(right wheel motor)
           左輪感測(left wheel sensor)     右輪感測(right wheel sensor) 
           接收器(reciver)

         F
     *********
     *       *
  |L|*       *|R|
     *       *
     *********
向前: L & R < 0
右轉: L < 0 & R > 0
向後: L & R > 0
左轉: L > 0 & R < 0