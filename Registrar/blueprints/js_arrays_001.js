var nums = new Array(), nums2;

for (let x = 0; x < 10; x++) {
	nums[x] = (x + 1);
}

console.log(nums);

nums2 = nums.map(function (data, index) {
	return index ** 2;
});

console.log("nums: " + nums);
console.log("nums2: " + nums2);