/*
 * The nested loops that appear in solution.cpp are an adequate solution to the
 * task, but scale very poorly. Thanks to freenode user Alipha in ##C++-general
 * for giving me this sample of code¹ showing how one might attack the general
 * problem. Their solution creates a indexing string of length N with exactly
 * C "1"s and then shuffles it. N.B. the initial order of this string matters 
 * because of std::next_permutation()'s lexicographic semantics.
 *
 * ¹also available at https://wandbox.org/permlink/dPk6ZQtlOrxAmwSy
 */

#include <iostream>

#include <algorithm>
#include <iterator>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>


namespace detail {
	template<typename It, typename ValueType>
	struct n_choose_k_iterator;
}


template<typename It, typename ValueType = std::vector<std::remove_reference_t<decltype(*std::declval<It>())>>>
struct n_choose_k {
	using value_type = ValueType;
	using iterator = detail::n_choose_k_iterator<It, ValueType>;
	
	
	n_choose_k(It n_first, It n_last, std::size_t k) : 
		first(std::move(n_first)), 
		last(std::move(n_last)), 
		k(k),
		n(last - first)
	{}
	
	iterator begin() {
		return iterator(this);
	}
	
	iterator end() {
		return iterator();
	}
	
private:
	template<typename I, typename V>
	friend struct detail::n_choose_k_iterator;
	
	It first;
	It last;
	std::size_t k;
	std::size_t n;
};


namespace detail {
	template<typename It, typename ValueType>
	struct n_choose_k_iterator {
		n_choose_k_iterator() : cont(nullptr), mask(), is_end(true) {}
		n_choose_k_iterator(const n_choose_k<It, ValueType> *cont) : cont(cont), mask(get_mask(cont->k, cont->n)), is_end(false) {}
		
		n_choose_k_iterator &operator++() {
			is_end = !std::next_permutation(mask.begin(), mask.end());
			return *this;
		}
		
		n_choose_k_iterator operator++(int) { auto ret = *this; ++ret; return ret; }
		
		n_choose_k_iterator &operator--() {
			is_end = !std::prev_permutation(mask.begin(), mask.end());
			return *this;
		}
		
		n_choose_k_iterator operator--(int) { auto ret = *this; --ret; return ret; }
		
		ValueType operator*() {
			ValueType out;
			auto src_it = cont->first;
			auto mask_it = mask.begin();
			
			for(; mask_it != mask.end(); ++mask_it, ++src_it)
				if(*mask_it == '1')
					out.push_back(*src_it);
					
			return out;
		}
		
		std::string get_mask(std::size_t k, std::size_t n) {
			if(k > n)
				throw std::out_of_range("n_choose_k: " + std::to_string(k) + " > " + std::to_string(n));
			return std::string(n - k, '0') + std::string(k, '1');
		}
		
		const n_choose_k<It, ValueType> *cont;
		std::string mask;
		bool is_end;
	};

	
	template<typename It, typename ValueType>
	bool operator==(const n_choose_k_iterator<It, ValueType> &left, const n_choose_k_iterator<It, ValueType> &right) {
		return left.is_end == right.is_end;   // TODO: more complex?
	}

	template<typename It, typename ValueType>
	bool operator!=(const n_choose_k_iterator<It, ValueType> &left, const n_choose_k_iterator<It, ValueType> &right) {
		return !(left == right);
	}
}



namespace std {
	template<typename It, typename ValueType>
	struct iterator_traits<detail::n_choose_k_iterator<It, ValueType>> {
		using difference_type = std::size_t;
		using value_type = ValueType;
		using reference = void;
		using pointer = void;
		using iterator_category = std::bidirectional_iterator_tag;
	};
}




int main() {
	std::vector<int> v = {2, 5, 9, 53, 29};
		
	for(auto e : n_choose_k(v.begin(), v.end(), 2)) {
		std::cout << e[0] << ", " << e[1] << std::endl;
	}
}
