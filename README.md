# 🔢 Đồ án cá nhân: 8-Puzzle Solver

## 🎯 Mục tiêu
Xây dựng một chương trình giải bài toán **8-Puzzle** sử dụng nhiều thuật toán tìm kiếm khác nhau trong lĩnh vực Trí tuệ nhân tạo.

---

## 🧠 Các thuật toán được triển khai
## Uninformed search algorithms

### 1. **Khái niệm chung về Uninformed Search Algorithms**
- **Uninformed Search** (tìm kiếm mù) là các thuật toán tìm kiếm không sử dụng thông tin heuristic (thông tin bổ sung về chi phí ước lượng đến mục tiêu). Chúng dựa vào cấu trúc của không gian tìm kiếm và các quy tắc cố định để khám phá các trạng thái.
- **Các thành phần chính**:
  - **Không gian trạng thái (State Space)**: Tập hợp tất cả các trạng thái có thể có của bài toán.
  - **Trạng thái ban đầu (Initial State)**: Điểm bắt đầu của bài toán.
  - **Trạng thái mục tiêu (Goal State)**: Trạng thái cần đạt được.
  - **Hành động (Actions)**: Các thao tác có thể thực hiện để chuyển từ trạng thái này sang trạng thái khác.
  - **Chi phí đường đi (Path Cost)**: Chi phí liên quan đến mỗi hành động hoặc đường đi (nếu có).
  - **Cấu trúc dữ liệu**: Thường sử dụng hàng đợi (queue), ngăn xếp (stack) hoặc hàng đợi ưu tiên (priority queue) để quản lý các trạng thái cần khám phá.

### 2. **Các thuật toán Uninformed Search**

#### a. **Breadth-First Search (BFS - Tìm kiếm theo chiều rộng)**
- **Mô tả**: Khám phá tất cả các trạng thái ở độ sâu hiện tại trước khi chuyển sang độ sâu tiếp theo. Sử dụng **hàng đợi (queue)** để lưu trữ các trạng thái.
- **Cách hoạt động**:
  1. Bắt đầu từ trạng thái ban đầu, thêm vào hàng đợi.
  2. Lấy trạng thái đầu tiên trong hàng đợi, kiểm tra xem có phải trạng thái mục tiêu không.
  3. Nếu không, sinh tất cả các trạng thái con (successors) và thêm chúng vào cuối hàng đợi.
  4. Lặp lại cho đến khi tìm thấy mục tiêu hoặc hàng đợi rỗng.
- **Đặc điểm**:
  - **Hoàn chỉnh (Complete)**: Tìm được giải pháp nếu tồn tại, với không gian trạng thái hữu hạn.
  - **Tối ưu (Optimal)**: Tìm đường đi ngắn nhất nếu chi phí hành động đồng nhất.
  - **Độ phức tạp**:
    - Thời gian: O(b^d), với b là số nhánh trung bình, d là độ sâu của giải pháp.
    - Không gian: O(b^d), do lưu trữ nhiều trạng thái ở mỗi mức.
- **Ứng dụng**: Tìm đường đi ngắn nhất trong đồ thị không trọng số, như mê cung.

#### b. **Depth-First Search (DFS - Tìm kiếm theo chiều sâu)**
- **Mô tả**: Khám phá trạng thái theo chiều sâu tối đa trước khi quay lại (backtrack). Sử dụng **ngăn xếp (stack)** hoặc đệ quy.
- **Cách hoạt động**:
  1. Bắt đầu từ trạng thái ban đầu, khám phá trạng thái con đầu tiên.
  2. Tiếp tục đi sâu vào một nhánh cho đến khi gặp ngõ cụt hoặc tìm thấy mục tiêu.
  3. Quay lại (backtrack) để khám phá các nhánh khác.
- **Đặc điểm**:
  - **Hoàn chỉnh**: Không đảm bảo trong không gian vô hạn hoặc có chu kỳ, trừ khi có cơ chế kiểm tra chu kỳ.
  - **Tối ưu**: Không tối ưu, vì có thể tìm đường đi dài hơn.
  - **Độ phức tạp**:
    - Thời gian: O(b^m), với m là độ sâu tối đa của không gian trạng thái.
    - Không gian: O(bm), do chỉ lưu một đường đi tại một thời điểm.
- **Ứng dụng**: Tìm kiếm trong không gian lớn, như giải câu đố, khi không cần đường đi tối ưu.

#### c. **Uniform Cost Search (UCS - Tìm kiếm chi phí đồng nhất)**
- **Mô tả**: Khám phá trạng thái theo chi phí đường đi tăng dần. Sử dụng **hàng đợi ưu tiên (priority queue)** dựa trên chi phí.
- **Cách hoạt động**:
  1. Bắt đầu từ trạng thái ban đầu, thêm vào hàng đợi ưu tiên với chi phí 0.
  2. Lấy trạng thái có chi phí thấp nhất từ hàng đợi, kiểm tra xem có phải mục tiêu không.
  3. Sinh các trạng thái con, tính chi phí đường đi từ gốc, thêm vào hàng đợi theo thứ tự chi phí.
  4. Lặp lại cho đến khi tìm thấy mục tiêu hoặc hàng đợi rỗng.
- **Đặc điểm**:
  - **Hoàn chỉnh**: Nếu chi phí hành động lớn hơn 0.
  - **Tối ưu**: Tìm đường đi có chi phí thấp nhất.
  - **Độ phức tạp**:
    - Thời gian: O(b^(C*/ε)), với C* là chi phí tối ưu, ε là chi phí hành động nhỏ nhất.
    - Không gian: O(b^(C*/ε)).
- **Ứng dụng**: Tìm đường đi tối ưu trong đồ thị có trọng số, như định tuyến đường đi.

#### d. **Iterative Deepening Search (IDS - Tìm kiếm sâu dần)**
- **Mô tả**: Kết hợp ưu điểm của BFS và DFS, thực hiện DFS với giới hạn độ sâu tăng dần.
- **Cách hoạt động**:
  1. Thực hiện DFS với giới hạn độ sâu (depth limit) là 0.
  2. Nếu không tìm thấy mục tiêu, tăng giới hạn độ sâu lên 1 và lặp lại.
  3. Tiếp tục tăng giới hạn độ sâu cho đến khi tìm thấy mục tiêu.
- **Đặc điểm**:
  - **Hoàn chỉnh**: Nếu không gian trạng thái hữu hạn.
  - **Tối ưu**: Tìm đường đi ngắn nhất nếu chi phí hành động đồng nhất.
  - **Độ phức tạp**:
    - Thời gian: O(b^d), tương tự BFS nhưng lặp lại nhiều lần.
    - Không gian: O(bd), tương tự DFS.
- **Ứng dụng**: Khi cần kết hợp ưu điểm của BFS (tối ưu) và DFS (tiết kiệm bộ nhớ).

### 3. **So sánh tổng quát**
| Thuật toán | Hoàn chỉnh | Tối ưu | Độ phức tạp thời gian | Độ phức tạp không gian | Ứng dụng chính |
|------------|------------|--------|-----------------------|------------------------|----------------|
| **BFS**    | Có (nếu hữu hạn) | Có (nếu chi phí đồng nhất) | O(b^d) | O(b^d) | Đường đi ngắn nhất (không trọng số) |
| **DFS**    | Không (nếu có chu kỳ) | Không | O(b^m) | O(bm) | Không gian lớn, không cần tối ưu |
| **UCS**    | Có (nếu chi phí > 0) | Có | O(b^(C*/ε)) | O(b^(C*/ε)) | Đường đi tối ưu (có trọng số) |
| **IDS**    | Có (nếu hữu hạn) | Có (nếu chi phí đồng nhất) | O(b^d) | O(bd) | Kết hợp BFS và DFS |

### 4. **Giải pháp tổng quát của Uninformed Search**
- **Quy trình chung**:
  1. Xác định trạng thái ban đầu và mục tiêu.
  2. Xây dựng không gian trạng thái và các hành động có thể thực hiện.
  3. Sử dụng cấu trúc dữ liệu (queue, stack, priority queue) để quản lý các trạng thái cần khám phá.
  4. Áp dụng chiến lược chọn trạng thái (theo chiều rộng, chiều sâu, chi phí, hoặc sâu dần) để tìm đường đi từ trạng thái ban đầu đến mục tiêu.
- **Ưu điểm**: Đơn giản, không cần thông tin bổ sung (heuristic), phù hợp với các bài toán không có thông tin về chi phí ước lượng.
- **Nhược điểm**: Hiệu quả thấp trong không gian trạng thái lớn hoặc phức tạp, đặc biệt khi không có heuristic hỗ trợ.

### 📷 **Hình ảnh các thuật toán được áp dụng trong trò chơi**
| **Thuật Toán**                  | **Minh Họa GIF**                                  |
|----------------------------------|---------------------------------------------------|
| **Breadth-First Search (BFS)**  | <img src="images/bfs.gif" width="500" alt="BFS">  |
| **Depth-First Search (DFS)**    | <img src="images/dfs.gif" width="500" alt="DFS">               |
| **Uniform Cost Search (UCS)**   | <img src="images/ucs.gif" width="500" alt="UCS">               |
| **Iterative Deepening Search (IDS)** | <img src="images/ids.gif" width="500" alt="IDS">         |

### 🔍 So sánh các thuật toán tìm kiếm không thông tin (Uninformed Search Algorithms)

| **Thuật toán** | **Hoàn chỉnh** | **Tối ưu** | **Bộ nhớ**       | **Thời gian**     | **Phù hợp với 8-puzzle**                                   |
|----------------|----------------|------------|------------------|-------------------|-------------------------------------------------------------|
| **BFS**        | Có             | Có         | Cao `O(b^d)`     | Cao `O(b^d)`      | ✔ Phù hợp nếu lời giải nông, nhưng tiêu tốn nhiều bộ nhớ    |
| **DFS**        | Không          | Không      | Thấp `O(bm)`     | Biến động `O(b^m)`| ❌ Không phù hợp, dễ bị kẹt và không tối ưu                 |
| **UCS**        | Có             | Có         | Cao `O(b^d)`     | Cao `O(b^d)`      | ✔ Tìm giải pháp tối ưu, nhưng tốn tài nguyên               |
| **IDS**        | Có             | Có         | Thấp `O(bd)`     | Cao `O(b^d)`      | ✔ Thích hợp khi bộ nhớ hạn chế, nhưng chậm hơn BFS          |

**Chú thích:**
- `b`: số nhánh trung bình (branching factor)
- `d`: độ sâu của lời giải tối ưu
- `m`: độ sâu tối đa của cây tìm kiếm

### 📝 Nhận xét chung:

Các thuật toán tìm kiếm không thông tin (Uninformed Search) đều không có kiến thức cụ thể về vị trí đích, do đó phải **duyệt toàn bộ không gian trạng thái một cách mù mờ**. Mỗi thuật toán có đặc điểm riêng:

* **BFS** thích hợp khi lời giải nằm ở độ sâu nhỏ, đảm bảo tìm được lời giải ngắn nhất nhưng **tốn nhiều bộ nhớ**.
* **DFS** có ưu điểm tiết kiệm bộ nhớ, nhưng **dễ rơi vào vòng lặp vô tận** và không đảm bảo tối ưu.
* **UCS** mở rộng BFS bằng cách tính đến chi phí, cho phép tìm lời giải tối ưu khi chi phí không đồng đều, nhưng **hiệu năng giảm nếu không gian tìm kiếm lớn**.
* **IDS** kết hợp ưu điểm của BFS và DFS: đảm bảo tối ưu, tiết kiệm bộ nhớ, nhưng **thời gian chạy lâu hơn do phải lặp lại nhiều lần**.

Với bài toán như **8-puzzle**, nơi không gian trạng thái lớn và cần lời giải tối ưu, **BFS, UCS hoặc IDS** là lựa chọn phù hợp. Tuy nhiên, khi bộ nhớ hạn chế, **IDS** thường là phương án an toàn hơn.

## Informed Search Algorithms

### 1. **Khái niệm chung về Informed Search Algorithms**
- **Informed Search** (tìm kiếm có thông tin) sử dụng **hàm heuristic** để ước lượng chi phí từ trạng thái hiện tại đến trạng thái mục tiêu, giúp định hướng tìm kiếm hiệu quả hơn so với Uninformed Search (BFS, DFS, UCS, IDS).
- **Các thành phần chính**:
  - **Không gian trạng thái (State Space)**: Tập hợp tất cả các trạng thái có thể có của bài toán (ví dụ: các hoán vị của ô trong 8-puzzle).
  - **Trạng thái ban đầu (Initial State)**: Điểm xuất phát của bài toán.
  - **Trạng thái mục tiêu (Goal State)**: Trạng thái cần đạt được.
  - **Hành động (Actions)**: Các thao tác hợp lệ để chuyển đổi giữa các trạng thái (ví dụ: di chuyển ô trống lên, xuống, trái, phải).
  - **Chi phí đường đi (Path Cost, g(n))**: Tổng chi phí từ trạng thái ban đầu đến trạng thái hiện tại (thường là số bước hoặc chi phí cụ thể của hành động).
  - **Hàm heuristic (h(n))**: Hàm ước lượng chi phí từ trạng thái hiện tại đến mục tiêu. Hàm này phải **admissible** (không overestimated) và lý tưởng là **consistent** (đáp ứng bất đẳng thức tam giác) để đảm bảo tính tối ưu.
  - **Cấu trúc dữ liệu**: Thường sử dụng hàng đợi ưu tiên (priority queue) để ưu tiên trạng thái có chi phí thấp nhất hoặc giá trị heuristic nhỏ nhất.

### 2. **Các thuật toán Informed Search**

#### a. **A* Search**
- **Mô tả**: A* sử dụng hàm đánh giá **f(n) = g(n) + h(n)**:
  - **g(n)**: Chi phí thực tế từ trạng thái ban đầu đến trạng thái hiện tại.
  - **h(n)**: Chi phí ước lượng từ trạng thái hiện tại đến mục tiêu (ví dụ: khoảng cách Manhattan trong 8-puzzle).
  - A* ưu tiên khám phá trạng thái có **f(n)** nhỏ nhất, đảm bảo đường đi tối ưu nếu heuristic là admissible.
- **Cách hoạt động**:
  1. Bắt đầu từ trạng thái ban đầu, thêm vào hàng đợi ưu tiên với chi phí `f(n) = g(n) + h(n)`.
  2. Lấy trạng thái có `f(n)` nhỏ nhất từ hàng đợi, kiểm tra xem có phải trạng thái mục tiêu không.
  3. Sinh các trạng thái con, tính `g(n)` và `h(n)` cho mỗi trạng thái, thêm vào hàng đợi.
  4. Lặp lại cho đến khi tìm thấy mục tiêu hoặc hàng đợi rỗng.
- **Đặc điểm**:
  - **Hoàn chỉnh**: Có, nếu không gian trạng thái hữu hạn và chi phí hành động lớn hơn 0.
  - **Tối ưu**: Có, nếu heuristic là admissible (h(n) ≤ chi phí thực tế đến mục tiêu).
  - **Độ phức tạp**:
    - Thời gian: O(b^d), nhưng thường nhanh hơn BFS/UCS nhờ heuristic định hướng.
    - Không gian: O(b^d), do lưu trữ nhiều trạng thái trong hàng đợi ưu tiên.
- **Ứng dụng**: Tìm đường đi tối ưu trong các bài toán như 8-puzzle, định tuyến, hoặc lập kế hoạch, khi cần đảm bảo chi phí thấp nhất.

#### b. **Iterative Deepening A* (IDA*)**
- **Mô tả**: IDA* kết hợp ý tưởng của A* và Iterative Deepening Search (IDS). Nó sử dụng hàm `f(n) = g(n) + h(n)` nhưng giới hạn tìm kiếm theo ngưỡng `f(n)` tăng dần, thực hiện tìm kiếm theo chiều sâu (DFS) trong mỗi lần lặp.
- **Cách hoạt động**:
  1. Bắt đầu với ngưỡng ban đầu là `f(n) = h(n)` của trạng thái ban đầu.
  2. Thực hiện DFS, chỉ khám phá các trạng thái có `f(n)` ≤ ngưỡng.
  3. Nếu không tìm thấy mục tiêu, tăng ngưỡng lên giá trị `f(n)` nhỏ nhất vượt ngưỡng hiện tại, lặp lại.
  4. Tiếp tục cho đến khi tìm thấy mục tiêu hoặc không còn trạng thái để khám phá.
- **Đặc điểm**:
  - **Hoàn chỉnh**: Có, nếu không gian trạng thái hữu hạn.
  - **Tối ưu**: Có, nếu heuristic là admissible.
  - **Độ phức tạp**:
    - Thời gian: O(b^d), nhưng có thể chậm hơn A* do lặp lại nhiều lần.
    - Không gian: O(bd), tiết kiệm bộ nhớ hơn A* vì chỉ lưu một đường đi tại mỗi lần lặp.
- **Ứng dụng**: Phù hợp cho các bài toán như 8-puzzle khi bộ nhớ hạn chế, nhưng cần giải pháp tối ưu.

#### c. **Greedy Best-First Search (Greedy)**
- **Mô tả**: Greedy ưu tiên khám phá trạng thái có giá trị **heuristic h(n)** nhỏ nhất, bỏ qua chi phí đường đi `g(n)`. Nó tập trung vào việc tiến gần trạng thái mục tiêu nhanh nhất có thể.
- **Cách hoạt động**:
  1. Bắt đầu từ trạng thái ban đầu, thêm vào hàng đợi ưu tiên với giá trị `h(n)`.
  2. Lấy trạng thái có `h(n)` nhỏ nhất, kiểm tra xem có phải mục tiêu không.
  3. Sinh các trạng thái con, tính `h(n)` cho mỗi trạng thái, thêm vào hàng đợi.
  4. Lặp lại cho đến khi tìm thấy mục tiêu hoặc hàng đợi rỗng.
- **Đặc điểm**:
  - **Hoàn chỉnh**: Không, có thể bị kẹt trong các vòng lặp hoặc bỏ sót giải pháp.
  - **Tối ưu**: Không, vì không xem xét chi phí đường đi `g(n)`, có thể dẫn đến đường đi dài hơn.
  - **Độ phức tạp**:
    - Thời gian: O(b^m), với m là độ sâu tối đa, nhưng thường nhanh hơn A* do chỉ dựa vào `h(n)`.
    - Không gian: O(b^m), tùy thuộc vào số trạng thái được lưu trữ.
- **Ứng dụng**: Dùng khi cần tìm giải pháp nhanh, không yêu cầu tối ưu, như trong một số bài toán tìm kiếm đơn giản hoặc khi thời gian thực thi là ưu tiên.

---

### 3. **So sánh tổng quát**
| Thuật toán | Hoàn chỉnh | Tối ưu | Độ phức tạp thời gian | Độ phức tạp không gian | Ứng dụng chính |
|------------|------------|--------|-----------------------|------------------------|----------------|
| **A***     | Có         | Có     | O(b^d)               | O(b^d)                | Tìm đường đi tối ưu (8-puzzle, định tuyến) |
| **IDA***   | Có         | Có     | O(b^d)               | O(bd)                 | Tìm đường đi tối ưu, tiết kiệm bộ nhớ |
| **Greedy** | Không      | Không  | O(b^m)               | O(b^m)                | Tìm giải pháp nhanh, không cần tối ưu |

---

### 4. **Giải pháp tổng quát của Informed Search**
- **Quy trình chung**:
  1. Xác định trạng thái ban đầu, trạng thái mục tiêu, và các hành động có thể thực hiện.
  2. Xây dựng hàm heuristic (ví dụ: khoảng cách Manhattan cho 8-puzzle) để ước lượng chi phí.
  3. Sử dụng hàng đợi ưu tiên hoặc chiến lược DFS với ngưỡng để quản lý các trạng thái cần khám phá.
  4. Áp dụng chiến lược chọn trạng thái:
     - **A***: Dựa trên `f(n) = g(n) + h(n)`.
     - **IDA***: DFS với ngưỡng `f(n)` tăng dần.
     - **Greedy**: Dựa trên `h(n)` nhỏ nhất.
  5. Tìm đường đi từ trạng thái ban đầu đến mục tiêu, ưu tiên các trạng thái có chi phí hoặc heuristic thấp.
- **Ưu điểm**:
  - Hiệu quả hơn Uninformed Search nhờ heuristic định hướng.
  - A* và IDA* đảm bảo tối ưu nếu heuristic là admissible.
  - IDA* tiết kiệm bộ nhớ, phù hợp cho các bài toán lớn.
  - Greedy nhanh, phù hợp khi không cần tối ưu.
- **Nhược điểm**:
  - A* tốn bộ nhớ do lưu trữ nhiều trạng thái.
  - IDA* có thể chậm do lặp lại nhiều lần.
  - Greedy không đảm bảo hoàn chỉnh hoặc tối ưu, dễ bị kẹt trong các cực trị cục bộ.
- **Yêu cầu**:
  - Cần thiết kế hàm heuristic phù hợp (admissible và consistent cho A* và IDA*).
  - Kiểm tra chu kỳ hoặc trạng thái lặp để tránh vòng lặp vô hạn.


### 📷 **Hình ảnh các thuật toán được áp dụng trong trò chơi**
| **Thuật Toán**                       | **Minh Họa GIF**                                      |
|-------------------------------------|-------------------------------------------------------|
| **A\* Search (A-Star)**             | <img src="images/astar.gif" width="500" alt="A*">     |
| **Iterative Deepening A\* (IDA\*)** | <img src="images/ida_star.gif" width="500" alt="IDA*">|
| **Greedy Best-First Search**        | <img src="images/greedy.gif" width="500" alt="Greedy">|


### 🔍 So sánh các thuật toán tìm kiếm có thông tin (Informed Search Algorithms)

| **Thuật Toán**        | **Hoàn chỉnh** | **Tối ưu** | **Độ phức tạp thời gian** | **Độ phức tạp không gian** | **Hiệu suất trong 8-puzzle**                                                                   | **Ưu điểm**                                       | **Nhược điểm**                                          |
| --------------------- | -------------- | ---------- | ------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------- |
| **A\***               | Có             | Có         | `O(b^d)`                  | `O(b^d)`                   | ✔ Hiệu quả cao, tìm đường đi ngắn nhất nhanh hơn BFS/UCS nhờ heuristic. Phù hợp khi đủ bộ nhớ. | ✅ Tối ưu, hoàn chỉnh, nhanh hơn Uninformed Search | ❌ Tốn nhiều bộ nhớ, giảm hiệu suất với độ sâu lớn (>20) |
| **IDA\***             | Có             | Có         | `O(b^d)`                  | `O(bd)`                    | ✔ Tiết kiệm bộ nhớ, phù hợp cho hệ thống hạn chế tài nguyên. Chậm hơn A\* ở độ sâu lớn.        | ✅ Tối ưu, tiết kiệm bộ nhớ                        | ❌ Chậm hơn A\* do phải lặp lại nhiều lần                |
| **Greedy Best-First** | Không          | Không      | `O(b^m)`                  | `O(b^m)`                   | ✔ Nhanh, nhưng dễ bị kẹt hoặc tìm đường không tối ưu. Phù hợp khi cần kết quả nhanh.           | ✅ Nhanh, đơn giản                                 | ❌ Không tối ưu, có thể bỏ sót lời giải tốt hơn          |

### **Chú thích:**
* `b`: Số nhánh trung bình (trong 8-puzzle, thường ≈ 2–4 tùy vị trí ô trống).
* `d`: Độ sâu của lời giải tối ưu.
* `m`: Độ sâu tối đa của không gian trạng thái.
* **Heuristic sử dụng**: *Khoảng cách Manhattan* là heuristic **admissible** và **consistent**, đảm bảo tính tối ưu cho thuật toán **A\*** và **IDA\***.

### 📝 **Nhận xét chung:**

Các thuật toán **tìm kiếm có thông tin (Informed Search)** như **A\***, **IDA\*** và **Greedy Best-First Search** tận dụng heuristic để hướng dẫn quá trình tìm kiếm hiệu quả hơn so với các thuật toán không thông tin.

* **A\*** là lựa chọn **tối ưu nhất** nếu hệ thống có đủ bộ nhớ, nhờ vào tính chất tối ưu và nhanh nhờ sử dụng heuristic tốt (ví dụ: Manhattan).
* **IDA\*** phù hợp cho các môi trường **hạn chế tài nguyên** (như thiết bị nhúng, bộ nhớ thấp), vẫn đảm bảo tối ưu nhưng **hy sinh tốc độ** vì phải lặp lại nhiều lần.
* **Greedy Best-First Search** hoạt động **nhanh và đơn giản**, tuy nhiên **thiếu tính tối ưu**, dễ rơi vào bẫy cục bộ (local minima) nếu heuristic không tốt.

👉 **Tóm lại**:

* Nếu **ưu tiên chất lượng lời giải** và **có đủ tài nguyên**, hãy chọn **A\***.
* Nếu **ưu tiên tiết kiệm bộ nhớ**, chọn **IDA\***.
* Nếu **cần kết quả nhanh** và **không quá quan tâm tối ưu**, có thể thử **Greedy**.











## 👨‍💻 Tác giả

**Nguyễn Trí Lâm**  
MSSV: `23110250`  
Môn: `Trí Tuệ Nhân Tạo`
Giáo viên hướng dẫn: `Phan Thị Huyền Trang` 

---
