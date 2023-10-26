function setup() {
  createCanvas(400, 400);
  background(255);
  translate(width / 2, height / 2);
  noLoop();
  noStroke();

  drawFlower(0, 'F2F2F2');        // 底层
  drawFlower(PI / 6, 'EBEBEB');   // 中间层
  drawFlower(0, '7C7C7C', 0.8);   // 顶层
}

function drawFlower(rotation, color, scale = 1) {
  push();
  rotate(rotation);
  scale(scale);
  fill(color);
  for (let i = 0; i < TWO_PI; i += TWO_PI / 6) {
    beginShape();
    let x1 = cos(i) * 50;
    let y1 = sin(i) * 50;
    let x2 = cos(i + TWO_PI / 6) * 50;
    let y2 = sin(i + TWO_PI / 6) * 50;
    let x3 = cos(i + TWO_PI / 12) * 80;
    let y3 = sin(i + TWO_PI / 12) * 80;
    let x4 = cos(i - TWO_PI / 12) * 80;
    let y4 = sin(i - TWO_PI / 12) * 80;
    vertex(x1, y1);
    vertex(x2, y2);
    vertex(x3, y3);
    vertex(x4, y4);
    endShape(CLOSE);
  }
  ellipse(0, 0, 100);
  pop();
}

