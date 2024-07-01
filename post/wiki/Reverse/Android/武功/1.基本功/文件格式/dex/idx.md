java -> class

class -> dex

```
dex -dex --output=HelloWorld.dex HelloWorld.class
 

vermeer:/data/local/tmp/dex $ ls
HelloWorld.dex
vermeer:/data/local/tmp/dex $ dalvikvm -cp ./HelloWorld.dex HelloWorld
Hello World
vermeer:/data/local/tmp/dex $

```



整体结构

```
> header
> stringArr
> typeArr
> protoArr
> fieldArr
> methodArr
> classArr
------------------------------------
> classData
------------------------------------
> mapArr
```



typeArr：stringArr 

protoArr：strArr+typeArr+argList_add

fieldArr：classArr + typeArr + strArr 

methodArr：classArr + protoArrArr + stringArr 

classArr: 



src: 

https://android.googlesource.com/platform/art/+/fc322c7/src/dex_file.h

https://android.googlesource.com/platform/art/+/kitkat-dev/runtime/dex_file.h

https://android.googlesource.com/platform/art/+/master/libdexfile/dex/dex_file.h

```c
  // Raw header_item.
  struct Header {
    uint8_t magic_[8];
    uint32_t checksum_;  // See also location_checksum_
    uint8_t signature_[kSha1DigestSize];
    uint32_t file_size_;  // size of entire file
    uint32_t header_size_;  // offset to start of next section
    uint32_t endian_tag_;
    uint32_t link_size_;  // unused
    uint32_t link_off_;  // unused
    uint32_t map_off_;  // unused
    uint32_t string_ids_size_;  // number of StringIds
    uint32_t string_ids_off_;  // file offset of StringIds array
    uint32_t type_ids_size_;  // number of TypeIds, we don't support more than 65535
    uint32_t type_ids_off_;  // file offset of TypeIds array
    uint32_t proto_ids_size_;  // number of ProtoIds, we don't support more than 65535
    uint32_t proto_ids_off_;  // file offset of ProtoIds array
    uint32_t field_ids_size_;  // number of FieldIds
    uint32_t field_ids_off_;  // file offset of FieldIds array
    uint32_t method_ids_size_;  // number of MethodIds
    uint32_t method_ids_off_;  // file offset of MethodIds array
    uint32_t class_defs_size_;  // number of ClassDefs
    uint32_t class_defs_off_;  // file offset of ClassDef array
    uint32_t data_size_;  // unused
    uint32_t data_off_;  // unused
  };
```







```c
struct string_def{
	byte str_length;//字符串长度
	byte str_data[1];//柔性数组，字符串内容，以0结尾
}
```



```c
// Raw proto_id_item.
struct ProtoId {
    uint32_t shorty_idx_;  // strArr的idx，字符串内容是对函数返回值和参数的简写
    uint32_t return_type_idx_;  // typeArr的idx,指明返回值类型
    uint32_t parameters_off_;  // 指向参数列表的文件偏移，指向的类型是class TypeList
};
// Raw type_list.
class TypeList {
private:
    uint32_t size_;  // 有多少个参数
    TypeItem list_[1];  // 柔性数组,基于typeArr的idx，指明的参数类型。    
public:
    uint32_t Size() const {//函数
      	return size_;
	}
	const TypeItem& GetTypeItem(uint32_t idx) const {//函数
        CHECK_LT(idx, this->size_);
        return this->list_[idx];
	}
};
```



```c
// Raw field_id_item.
struct FieldId {
    uint16_t class_idx_;  //基于typeArr的idx，说明该成员属于哪一个类！！！
    uint16_t type_idx_;  //基于typeArr的idx，指明该成员是什么类型
    uint32_t name_idx_;  //基于strArr的idx，指明成员的名字
};
```



```c
// Raw method_id_item.
struct MethodId {
    uint16_t class_idx_;  // 基于typeArr的idx，说明该函数属于哪一个类 ！！！
    uint16_t proto_idx_;  // 基于protoArr的idx，说明该函数的类型
    uint32_t name_idx_;  // 基于srtArr的idx，说明该函数的名字
};
```



```c
// Raw class_def_item.
struct ClassDef {
    uint32_t class_idx_;  // 基于typeArr的idx，说明该函数属于哪一个类 ！！！
    uint32_t access_flags_; //常量值，类似于final，public，private…之类的
    uint32_t superclass_idx_;  // 基于typeArr的idx，说明父类的类型
    uint32_t interfaces_off_;  // file offset to TypeList,接口相关
    uint32_t source_file_idx_;  // 基于strArr的idx，说明源代码文件的名字
    uint32_t annotations_off_;  // file offset to annotations_directory_item
    uint32_t class_data_off_;  // class_data_item 结构体的文件偏移
    uint32_t static_values_off_;  // file offset to EncodedArray
};

```



```c
struct static_field sfArr{
    byte field_idx_diff;
    byte access_flags;//常量值，
}
struct direct_method{
    byte method_idx_diff;
    byte access_flags[1];//我也不着调这个大小有多长
    word(struct code*) code_off;
}
struct class_data{
    byte static_fields_size;
    byte instance_fields_size;
    byte direct_methods_size;
    byte virtual_methods_size;
    struct static_field sfArr[1];//柔性数组，成员个数由static_fields_size决定。
    struct instance_field iffArr[1];//柔性数组，成员个数由instance_fields_size决定。
    struct direct_methods dmArr[1];//柔性数组，成员个数由direct_methods_size决定。
    struct virtual_methods vmArr[1];//柔性数组，成员个数由virtual_methods_size决定。
	
}
  // Raw code_item.
  struct CodeItem {
    uint16_t registers_size_;
    uint16_t ins_size_;
    uint16_t outs_size_;
    uint16_t tries_size_;
    uint32_t debug_info_off_;  // file offset to debug info stream
    uint32_t insns_size_;  // size of the insns array, in 2 byte code units
    uint16_t insns_[1];
  };
```



```c
  struct MapItem {
    uint16_t type_;//常量值，该区域是什么类型
    uint16_t unused_;
    uint32_t size_;
    uint32_t offset_; //区域的文件偏移，开始地址
   private:
    DISALLOW_COPY_AND_ASSIGN(MapItem);
  };
  struct MapList {
    uint32_t size_;
    MapItem list_[1];
   private:
    DISALLOW_COPY_AND_ASSIGN(MapList);
  };
```

